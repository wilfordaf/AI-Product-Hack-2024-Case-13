from typing import Dict, List

from service.custom_typing.endpoint_types.ping_response_body_type import (
    TPingResponseBody,
)
from service.utils.logging import ConsoleLogger


class DataFormattingController:
    def __init__(self, api_version: str):
        self._api_version: Dict[str, str] = {"api_version": api_version}
        self._logger = ConsoleLogger()

    def format_ping_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._api_version | {"model_{i}": model_info for i, model_info in enumerate(models_info, 1)}

    @staticmethod
    def format_ping_response_body() -> TPingResponseBody:
        return {"ping": "OK!"}
