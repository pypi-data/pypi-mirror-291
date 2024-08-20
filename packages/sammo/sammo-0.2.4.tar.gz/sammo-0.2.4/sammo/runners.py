# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from __future__ import annotations
import base64
import re
import warnings
from abc import abstractmethod
import asyncio
import async_timeout
from collections.abc import MutableMapping
import json
import logging
import os
import pathlib
from contextlib import asynccontextmanager

import aiohttp
import orjson
from beartype import beartype
from beartype.typing import Literal, Union

from sammo import PROMPT_LOGGER_NAME
from sammo.base import LLMResult, Costs, Runner
from sammo.store import PersistentDict, SqlLiteDict
from sammo.throttler import AtMost, Throttler
from sammo.utils import serialize_json

logger = logging.getLogger(__name__)
prompt_logger = logging.getLogger(PROMPT_LOGGER_NAME)


class RetriableError(Exception):
    pass


class NonRetriableError(Exception):
    pass


class MockedRunner(Runner):
    def __init__(self, return_values=""):
        self._ret_vals = return_values
        self._n_calls = -1
        self.prompt_log = list()

    async def generate_text(self, prompt: str, *args, **kwargs):
        self._n_calls += 1
        self.prompt_log.append(prompt)
        if isinstance(self._ret_vals, list):
            ret_val = self._ret_vals[self._n_calls % len(self._ret_vals)]
        else:
            ret_val = self._ret_vals
        return LLMResult(ret_val, costs=Costs(), request_text=prompt)


class BaseRunner(Runner):
    """Base class for OpenAI API runners.

    :param model_id: Model specifier as listed in the API documentation.
    :param cache: A dict-like object to use for storing results.
    :param api_config: The path to the API config file or a dictionary containing the API information.
    :param rate_limit: The rate limit to use. If an integer, it specifies max calls per second.
    :param max_retries: The maximum number of retries to attempt.
    :param debug_mode: Enable debug mode where queries do not get issued.
    :param retry: Enable retrying when retriable error is raised (defined in each subclass).
    :param timeout: The timeout (in s) to use for a query.
    :param max_context_window: The maximum number of tokens to use for the context window. Defaults to None, which
    means that the maximum context window is used.
    :param max_timeout_retries: The maximum number of retries to attempt when a timeout occurs.
    :param use_cached_timeouts: Whether to use cached timeouts.
    """

    RETRY_ERRORS = ()
    DEFAULT_CACHE = PersistentDict

    def __init__(
        self,
        model_id: str,
        api_config: dict | str | pathlib.Path,
        cache: Union[None, MutableMapping, str, os.PathLike] = None,
        equivalence_class: Union[str, Literal["major", "exact"]] = "major",
        rate_limit: Union[AtMost, list[AtMost], Throttler, int] = 2,
        max_retries: int = 50,
        max_context_window: Union[int, None] = None,
        retry: bool = True,
        timeout: Union[float, int] = 60,
        max_timeout_retries: int = 1,
        use_cached_timeouts: bool = True,
    ):
        super().__init__()

        if isinstance(api_config, dict):
            self._api_config = dict(api_config)
        elif isinstance(api_config, str):
            with open(api_config) as api_config_file:
                self._api_config = json.load(api_config_file)
        elif isinstance(api_config, pathlib.Path):
            with api_config.open() as api_config_file:
                self._api_config = json.load(api_config_file)
        if isinstance(rate_limit, Throttler):
            self._throttler = rate_limit
        elif isinstance(rate_limit, AtMost):
            self._throttler = Throttler(limits=[rate_limit])
        else:
            if isinstance(rate_limit, int):
                rate_limit = [AtMost(rate_limit, "calls", period=1)]
            self._throttler = Throttler(limits=rate_limit)

        self._model_id = model_id

        if equivalence_class == "major":
            self._equivalence_class = self._get_equivalence_class(self._model_id)
        elif equivalence_class == "exact":
            self._equivalence_class = self._model_id
        else:
            self._equivalence_class = equivalence_class

        if isinstance(cache, str) or isinstance(cache, os.PathLike):
            self._cache = self.DEFAULT_CACHE(cache)
        else:
            self._cache = cache
        self._retry_on = RetriableError if retry else tuple()
        self._max_retries = max_retries
        self._semaphores = dict()
        self._timeout = timeout
        self._max_timeout_retries = max_timeout_retries
        self._max_context_window = max_context_window
        self._use_cached_timeouts = use_cached_timeouts
        self._post_init()

    async def _execute_request(self, request, fingerprint, priority=0):
        if fingerprint in self._semaphores:
            sem = self._semaphores[fingerprint]
        else:
            sem = asyncio.Semaphore(1)
            self._semaphores[fingerprint] = sem
        async with sem:
            # important: ensure that we do not run the same prompt concurrently
            if self._cache is not None and fingerprint in self._cache:
                record = self._cache[fingerprint]
                if self._use_cached_timeouts and isinstance(record, dict) and "sammo.error.timeout" in record:
                    # re-raise the timeout error if the timeout is the same or higher
                    if self._timeout <= record["sammo.error.timeout"]["timeout"]:
                        raise TimeoutError("Cached timeout")
                else:
                    json = self._cache[fingerprint]
                    response_obj = self._augmented_llm_result(request, json, fingerprint)
                    self._costs += response_obj.costs
                    return response_obj

            n_timeouts = 0
            for cur_try in range(self._max_retries):
                retry_on = self._retry_on if cur_try < self._max_retries - 1 else tuple()

                try:
                    job_handle = await self._throttler.wait_in_line(priority)
                    async with async_timeout.timeout(self._timeout):
                        json = await self._call_backend(request)
                    response_obj = self._augmented_llm_result(request, json, fingerprint)
                    response_obj.retries = cur_try
                    self._throttler.update_job_stats(job_handle, cost=response_obj.costs.total)
                    self._costs += response_obj.costs
                    if self._cache is not None:
                        self._cache[fingerprint] = json
                    return response_obj
                except TimeoutError:
                    n_timeouts += 1
                    self._throttler.update_job_stats(job_handle, failed=True, cost=0)
                    logger.error(f"TimeoutError: {request}")
                    if n_timeouts > self._max_timeout_retries:
                        self._cache[fingerprint] = {
                            "sammo.error.timeout": {"retries": cur_try, "timeout": self._timeout}
                        }
                        raise TimeoutError
                    continue
                except retry_on as e:
                    qualified_name = f"{type(e).__module__}.{type(e).__name__}".replace("builtins.", "")
                    self._throttler.update_job_stats(job_handle, failed=True, cost=0)
                    logger.error(f"{qualified_name}: {str(e).split(' Contact us')[0]}")
                    continue

            raise RuntimeError(f"Could not get completion for {request.params}")

    def _augmented_llm_result(self, request: dict, json_data: dict, fingerprint: str | bytes) -> LLMResult:
        result = self._to_llm_result(request, json_data, fingerprint)
        result.fingerprint = fingerprint
        result.extra_data = json_data
        return result

    @abstractmethod
    def _to_llm_result(self, request: dict, json_data: dict, fingerprint: str | bytes) -> LLMResult:
        pass

    @abstractmethod
    async def _call_backend(self, request: dict) -> dict:
        pass

    @classmethod
    def _get_equivalence_class(cls, model_id: str) -> str:
        return model_id

    @asynccontextmanager
    async def _get_session(self):
        async with aiohttp.ClientSession(
            json_serialize=lambda x: orjson.dumps(x).decode(), timeout=aiohttp.ClientTimeout(None, None, None)
        ) as session:
            yield session

    def _get_headers(self):
        return {}

    def _post_init(self):
        pass

    def _rest_url(self):
        return (self._api_config.get("base_url", None) or self.BASE_URL) + self.SUFFIX

    @staticmethod
    def _purge_none_values(d: dict):
        return {k: v for k, v in d.items() if v is not None}


class RestRunner(BaseRunner):
    async def _call_backend(self, request: dict) -> dict:
        async with self._get_session() as session:
            async with session.post(
                self._rest_url(),
                json=request,
                headers=self._get_headers(),
            ) as response:
                text = await response.json()
                if response.status in [429, 500, 503, 529]:
                    raise RetriableError(f"Server error: {response.status} {text}")
                elif response.status == 200:
                    return text
                else:
                    raise NonRetriableError(f"Server error: {response.status} {text}")


class OpenAIBaseRunner(RestRunner):
    @classmethod
    def _get_equivalence_class(cls, model_id: str) -> str:
        if model_id.startswith("gpt-3"):
            return "gpt-3"
        elif model_id.startswith("gpt-4"):
            return "gpt-4"
        else:
            return model_id

    def _get_headers(self):
        return {"Authorization": f"Bearer {self._api_config['api_key']}"}


class OpenAIChat(OpenAIBaseRunner):
    BASE_URL = "https://api.openai.com/v1"
    SUFFIX = "/chat/completions"

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int | None = None,
        randomness: float | None = 0,
        seed: int = 0,
        priority: int = 0,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
        json_mode: bool = False,
    ) -> LLMResult:
        """Calls the chat endpoint of the OAI model.

        Args:
            prompt: The user prompt.
            max_tokens: The maximum number of tokens to generate. If not set, corresponds to maximum
            available tokens.
            randomness: The randomness to use when generating tokens.
            seed: When using randomness, use this seed for local reproducibility (achieved by caching).
            priority: The priority of the request (used for throttling).

        Returns:
            Dictionary with keys "data" (the generated text), "cost" (the number of tokens used),
            and "retries" (the number of retries).
        """
        messages = []
        if system_prompt is not None:
            messages = [{"role": "system", "content": system_prompt}]
            if history:
                history = [x for x in history if x["role"] != "system"]
        if history is not None:
            messages = messages + history

        # check for images in prompt
        revised_prompt = self._post_process_prompt(prompt)
        messages += [{"role": "user", "content": revised_prompt}]

        request = dict(messages=messages, max_tokens=self._max_context_window or max_tokens, temperature=randomness)
        if json_mode:
            request["response_format"] = {"type": "json_object"}
        fingerprint = serialize_json({"seed": seed, "generative_model_id": self._equivalence_class, **request})

        return await self._execute_request(request | {"model": self._model_id}, fingerprint, priority)

    def _to_llm_result(self, request: dict, json_data: dict, fingerprint: str | bytes) -> LLMResult:
        request_text = request["messages"][-1]["content"]
        prompt_logger.debug(f"\n\n\nAPI call:\n{request_text}\n->\n\n{json_data['choices'][0]['message']['content']}")
        return LLMResult(
            json_data["choices"][0]["message"]["content"],
            history=request["messages"] + [json_data["choices"][0]["message"]],
            costs=self._extract_costs(json_data),
            request_text=request["messages"][-1]["content"],
        )

    def _post_process_prompt(self, prompt: str):
        return prompt

    @staticmethod
    def _extract_costs(json_data: dict) -> dict:
        return Costs(
            input_costs=json_data["usage"].get("prompt_tokens", 0),
            output_costs=json_data["usage"].get("completion_tokens", 0),
        )


class AzureMixIn:
    """Mix-in class for Azure API runners.

    :param api_config: The path to the API config file or a dictionary containing the API information.
    Should be of the form: {'api_key': ??, 'endpoint': 'https://??.openai.azure.com/', 'deployment_id': ??}.
    """

    def _post_init(self):
        if not "endpoint" in self._api_config:
            raise ValueError("Azure API needs an endpoint.")
        if not "deployment_id" in self._api_config:
            warnings.warn(f"Missing deployment_id, using model_id {self._model_id}.")
        if not "api_version" in self._api_config:
            warnings.warn("API Version not given, assuming " "2023-05-15" ".", UserWarning)
            self._api_config["api_version"] = "2023-05-15"
        if self._api_config["endpoint"].endswith("/"):
            self._api_config["endpoint"] = self._api_config["endpoint"][:-1]

    def _get_headers(self):
        return {"api-key": self._api_config["api_key"], "Content-Type": "application/json"}

    def _rest_url(self):
        return (
            f"{self._api_config['endpoint']}/openai/deployments/{self._api_config['deployment_id']}"
            f"/{self.SCENARIO}?api-version={self._api_config['api_version']}"
        )


class OpenAIVisionChat(OpenAIChat):
    def _post_init(self):
        super()._post_init()
        if self._max_context_window is None:
            raise ValueError("Vision model needs explicit max_token_window value.")

    def _post_process_prompt(self, prompt: str):
        segmented_prompt = self.find_image_segments(prompt)
        if len(segmented_prompt) == 1 and isinstance(segmented_prompt[0], str):
            return prompt
        else:
            revised_prompt = list()
            for segment in segmented_prompt:
                if isinstance(segment, re.Match):
                    revised_prompt.append(self.load_image(segment.group("src")))
                else:
                    revised_prompt.append({"type": "text", "text": segment})
            return revised_prompt

    @classmethod
    def find_image_segments(cls, text):
        matches = re.finditer(r"{{image (?P<src>[^}]+)}}", text, re.MULTILINE)
        current = 0
        parsed_segments = list()
        for m in matches:
            if m.start() > current:
                parsed_segments.append(text[current : m.start()])
            current = m.end()
            parsed_segments.append(m)
        if current < len(text) or len(text) == 0:
            parsed_segments.append(text[current:])
        return parsed_segments

    @classmethod
    def load_image(cls, img_src):
        if img_src.startswith("https://") or img_src.startswith("http://"):
            img_data = img_src
        else:
            file = pathlib.Path(img_src)
            mediatype = "jpeg" if re.match(r"jpe?p", file.suffix[1:].lower()) else file.suffix[1:].lower()
            with open(file, "rb") as image_file:
                img_data = f"data:image/{mediatype};base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
        return {"type": "image_url", "image_url": {"url": img_data}}


class OpenAIEmbedding(OpenAIChat):
    SUFFIX = "/embeddings"
    INPUT_FIELD = "input"
    DEFAULT_CACHE = SqlLiteDict

    def _post_init(self):
        super()._post_init()
        self._embeddings_cache = self._cache
        self._cache = None

    async def generate_embedding(self, text: str | list[str], priority: int = 0) -> LLMResult:
        if isinstance(text, list) and len(text) > 2048:
            raise ValueError("Batch size must be below 2048.")
        elif not isinstance(text, list):
            text = [text]

        # Look up the cache for the embeddings
        embeddings = [None] * len(text)
        missing = list()
        for i, t in enumerate(text):
            if self._embeddings_cache is not None and (self._equivalence_class, t) in self._embeddings_cache:
                embeddings[i] = self._embeddings_cache[(self._equivalence_class, t)]
            else:
                missing.append(i)
        if missing:
            fingerprint = serialize_json({"embedding_model_id": self._equivalence_class, self.INPUT_FIELD: text})
            missing_embeddings = await self._execute_request(
                {self.INPUT_FIELD: [text[i] for i in missing], "model": self._model_id}, fingerprint, priority
            )
            for i, emb in zip(missing, missing_embeddings.value):
                embeddings[i] = emb
                if self._embeddings_cache is not None:
                    self._embeddings_cache[(self._equivalence_class, text[i])] = emb
        return LLMResult(embeddings, costs=Costs())

    def _to_llm_result(self, request: dict, json_data: dict, fingerprint: str | bytes):
        return LLMResult([x["embedding"] for x in json_data["data"]], costs=self._extract_costs(json_data))


class AzureChat(AzureMixIn, OpenAIChat):
    SCENARIO = "chat/completions"


class AzureVisionChat(AzureMixIn, OpenAIVisionChat):
    SCENARIO = "chat/completions"


class AzureEmbedding(AzureMixIn, OpenAIEmbedding):
    SCENARIO = "embeddings"


class GeminiChat(RestRunner):
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/"
    SUFFIX = ":generateContent"

    def _get_headers(self):
        return {"x-goog-api-key": self._api_config["api_key"], "Content-Type": "application/json"}

    def _rest_url(self):
        return f"{self.BASE_URL}{self._model_id}{self.SUFFIX}"

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int | None = None,
        randomness: float | None = 0,
        seed: int = 0,
        priority: int = 0,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
        json_mode: bool = False,
    ) -> LLMResult:
        """Calls the chat endpoint of Gemini

        Args:
            prompt: The user prompt.
            max_tokens: The maximum number of tokens to generate. If not set, corresponds to maximum
            available tokens.
            randomness: The randomness to use when generating tokens.
            seed: When using randomness, use this seed for local reproducibility (achieved by caching).
            priority: The priority of the request (used for throttling).

        Returns:
            Dictionary with keys "data" (the generated text), "cost" (the number of tokens used),
            and "retries" (the number of retries).
        """
        messages = []
        if history is not None:
            messages += history
        messages += [{"role": "user", "parts": [{"text": prompt}]}]

        request = dict(
            contents=messages,
            generationConfig=dict(maxOutputTokens=self._max_context_window or max_tokens, temperature=randomness),
        )
        if system_prompt is not None:
            request["system_instruction"] = {"parts": [{"text": system_prompt}]}
        if json_mode:
            request["generationConfig"]["responseMimeType"] = "application/json"

        fingerprint = serialize_json({"seed": seed, "generative_model_id": self._equivalence_class, **request})

        return await self._execute_request(request, fingerprint, priority)

    def _to_llm_result(self, request: dict, json_data: dict, fingerprint: str | bytes) -> LLMResult:
        request_text = request["contents"][-1]["parts"][0]["text"]
        response = json_data["candidates"][0]["content"]["parts"][0]
        response_text = response["text"]
        usage = json_data["usageMetadata"]
        prompt_logger.debug(f"\n\n\nAPI call:\n{request_text}\n->\n\n{response_text}")
        return LLMResult(
            response_text,
            history=request["contents"] + [response],
            costs=Costs(usage["promptTokenCount"], usage["candidatesTokenCount"]),
            request_text=request_text,
        )


class AnthropicChat(RestRunner):
    BASE_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def _post_init(self):
        if "anthropic-version" not in self._api_config:
            warnings.warn(f"'anthropic-version' not given, assuming '{self.API_VERSION}'.", UserWarning)
            self._api_config["anthropic-version"] = self.API_VERSION
        if self._max_context_window is None:
            warnings.warn("Max context window not given, assuming 4096.", UserWarning)
            self._max_context_window = 4096

    def _get_headers(self):
        return {
            "x-api-key": self._api_config["api_key"],
            "content-type": "application/json",
            "anthropic-version": self._api_config["anthropic-version"],
        }

    def _rest_url(self):
        return self.BASE_URL

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int | None = None,
        randomness: float | None = 0,
        seed: int = 0,
        priority: int = 0,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
        json_mode: bool = False,
    ) -> LLMResult:
        """Calls the chat endpoint of Gemini

        Args:
            prompt: The user prompt.
            max_tokens: The maximum number of tokens to generate. If not set, corresponds to maximum
            available tokens.
            randomness: The randomness to use when generating tokens.
            seed: When using randomness, use this seed for local reproducibility (achieved by caching).
            priority: The priority of the request (used for throttling).

        Returns:
            Dictionary with keys "data" (the generated text), "cost" (the number of tokens used),
            and "retries" (the number of retries).
        """
        messages = []
        if history is not None:
            messages += history
        messages += [{"role": "user", "content": prompt}]

        request = self._purge_none_values(
            dict(
                messages=messages,
                max_tokens=max_tokens or self._max_context_window,
                temperature=randomness,
                system=system_prompt,
            )
        )
        if json_mode:
            raise NotImplementedError("JSON mode not supported for Anthropic models.")

        fingerprint = serialize_json({"seed": seed, "generative_model_id": self._equivalence_class, **request})

        return await self._execute_request(request | {"model": self._model_id}, fingerprint, priority)

    def _to_llm_result(self, request: dict, json_data: dict, fingerprint: str | bytes) -> LLMResult:
        request_text = request["messages"][-1]["content"]
        response = json_data["content"][0]
        response_text = response["text"]
        usage = json_data["usage"]
        prompt_logger.debug(f"\n\n\nAPI call:\n{request_text}\n->\n\n{response_text}")
        return LLMResult(
            response_text,
            history=request["messages"] + [response],
            costs=Costs(usage["input_tokens"], usage["output_tokens"]),
            request_text=request_text,
        )
