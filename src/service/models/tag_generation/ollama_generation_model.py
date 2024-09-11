import importlib
import os
from pathlib import Path
from typing import List

import requests

from src.service.models.tag_generation.interfaces import ITagGenerationModel
from src.service.utils.exceptions.service_error import ServiceError
from src.service.utils.logging import ConsoleLogger


class OllamaGenerationModel(ITagGenerationModel):
    _OLLAMA_URL_VAR_NAME = "OLLAMA_URL"
    _PARAMS = {
        "stream": False,
        "model": "jpacifico/chocolatine-3b",
        "system": "You are a helpful assistant. You must provide complete and clear answers.",
    }
    _PROMPT_PATH = Path(__file__).parent.resolve() / "prompts/test_prompt.txt"
    _REQUEST_TIMEOUT = 2 * 60

    def __init__(self, possible_tags: List[str]):
        self._raw_connection_string = os.getenv(self._OLLAMA_URL_VAR_NAME, "http://localhost:11434")
        self._generate_connection_string = f"{self._raw_connection_string}/api/generate"
        try:
            self._version = getattr(importlib.import_module(".".join(self.__module__.split(".")[:-1])), "version")
        except AttributeError as e:
            raise ServiceError("Module does not have version.py or it is not in __init__.py") from e
        except ValueError as e:
            raise ServiceError(f"Incorrect path to {self.__module__}") from e

        try:
            self._prompt = open(self._PROMPT_PATH, encoding="utf-8").read()
        except FileNotFoundError as e:
            raise ServiceError("File with prompt is not found") from e

        self._possible_tags = possible_tags
        self._logger = ConsoleLogger()

    @property
    def info(self) -> str:
        return f"OllamaGenerationModel v{self._version}"

    def load_model(self) -> None:
        try:
            status_code = requests.get(self._raw_connection_string, timeout=2).status_code
        except requests.exceptions.RequestException as e:
            raise ServiceError(f"Ollama server is not on {self._raw_connection_string}") from e

        if status_code != 200:
            raise ServiceError("Ollama installation is not proper")

    def generate_tags(self, text: str) -> List[str]:
        self._logger.debug(f"Generating tags for {text}")
        try:
            response: str = requests.post(
                self._generate_connection_string,
                json={**self._PARAMS, "prompt": text},
                timeout=self._REQUEST_TIMEOUT,
            ).json()["response"]
        except requests.RequestException as e:
            raise ServiceError("Encountered network error requesting ollama") from e
        except KeyError as e:
            raise ServiceError(f"Incorrect response format: {e}") from e

        return self._parse_response(response)

    def _parse_response(self, response: str) -> List[str]:
        return list(set(tag for tag in self._possible_tags if tag in response))
