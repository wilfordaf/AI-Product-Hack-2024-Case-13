import importlib
from pathlib import Path
from typing import List

import requests

from service.models.tag_generation.interfaces import ITagGenerationModel
from service.utils.exceptions.service_error import ServiceError
from service.utils.logging import ConsoleLogger


class OllamaGenerationModel(ITagGenerationModel):
    _OLLAMA_URL = "http://localhost:11434/api/generate"
    # TODO: подобрать модель
    _PARAMS = {
        "stream": False,
        "model": "llama3.1-8B",
        "system": "You are a helpful assistant. You must provide complete and clear answers.",
    }
    _PROMPT_PATH = Path(__file__).parent.resolve() / "prompts/test_prompt.txt"
    _REQUEST_TIMEOUT = 2 * 60

    def __init__(self, possible_tags: List[str]):
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

    def generate_tags(self, text: str) -> List[str]:
        self._logger.debug(f"Generating tags for {text}")
        try:
            response: str = requests.post(
                self._OLLAMA_URL,
                json={**self._PARAMS, "prompt": text},
                timeout=self._REQUEST_TIMEOUT,
            ).json()["response"]
        except requests.RequestException as e:
            raise ServiceError("Encountered network error requesting ollama") from e
        except KeyError as e:
            raise ServiceError(f"Incorrect response format: {e}") from e

        return self._parse_response(response)

    def _parse_response(self, response: str) -> List[str]:
        return [tag for tag in self._possible_tags if tag in response]
