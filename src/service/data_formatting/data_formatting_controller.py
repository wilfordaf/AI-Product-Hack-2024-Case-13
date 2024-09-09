from typing import Dict, List

from service.entities.api_models.input.add_tags_user_request_body import (
    AddTagsUserRequestBody,
)
from src.service.custom_typing.endpoint_types import (
    TPingResponseBody,
    TSuccessResponseBody,
)
from src.service.database_interaction.dto.user import UserCreateDTO, UserUpdateTagsDTO
from src.service.entities.api_models.input import AddUserRequestBody
from src.service.utils.logging import ConsoleLogger


class DataFormattingController:
    def __init__(self, api_version: str):
        self._api_version: Dict[str, str] = {"api_version": api_version}
        self._logger = ConsoleLogger()

    def format_ping_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_ping_response_body() -> TPingResponseBody:
        return {"ping": "OK!"}

    def format_add_user_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_add_user_response_body(success: bool) -> TSuccessResponseBody:
        return {"success": success}

    def format_add_tags_to_user_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_add_tags_to_user_user_response_body(success: bool) -> TSuccessResponseBody:
        return {"success": success}

    def get_user_create_dto_by_request_body(self, request_body: AddUserRequestBody) -> UserCreateDTO:
        return UserCreateDTO(telegram_id=request_body.telegram_id)

    def get_user_update_dto_by_request_body(self, request_body: AddTagsUserRequestBody) -> UserUpdateTagsDTO:
        return UserUpdateTagsDTO(telegram_id=request_body.telegram_id, tag_titles=request_body.tags)

    def _format_base_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._api_version | {"model_{i}": model_info for i, model_info in enumerate(models_info, 1)}
