from typing import Dict, List, Tuple

from src.service.custom_typing.endpoint_types import (
    TPingResponseBody,
    TSuccessResponseBody,
    TTagTitlesResponse,
    TUserRankingResponseBody,
)
from src.service.database_interaction.dto.event import (
    EventCreateDTO,
    EventUpdateUserDTO,
)
from src.service.database_interaction.dto.tag import TagDTO
from src.service.database_interaction.dto.user import (
    UserCreateDTO,
    UserDTO,
    UserUpdateTagsDTO,
)
from src.service.entities.api_models.input import (
    AddEventRequestBody,
    AddUserRequestBody,
)
from src.service.entities.api_models.input.add_user_to_event_request_body import (
    AddUserToEventRequestBody,
)
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
    def format_add_tags_to_user_response_body(success: bool) -> TSuccessResponseBody:
        return {"success": success}

    def format_get_ranking_user_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_get_ranking_user_response_body(ranking_result: List[Tuple[str, List[str]]]) -> TUserRankingResponseBody:
        return {"users": [{"telegram_id": telegram_id, "tags": tags} for telegram_id, tags in ranking_result]}

    def format_get_event_users_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_get_event_users_response_body(users: List[UserDTO]) -> TUserRankingResponseBody:
        return {"users": [{"telegram_id": user.telegram_id, "tags": user.tags} for user in users]}

    def format_get_is_admin_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_get_is_admin_response_body(is_admin: bool) -> TSuccessResponseBody:
        return {"success": is_admin}

    def format_get_tags_by_user_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_get_tags_by_user_response_body(tags: List[TagDTO]) -> TTagTitlesResponse:
        return {"tags": [tag.title for tag in tags]}

    def format_add_event_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_add_event_response_body(success: bool) -> TSuccessResponseBody:
        return {"success": success}

    def format_add_user_to_event_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._format_base_response_header(models_info)

    @staticmethod
    def format_add_user_to_event_response_body(success: bool) -> TSuccessResponseBody:
        return {"success": success}

    def get_user_create_dto_by_request_body(self, request_body: AddUserRequestBody) -> UserCreateDTO:
        return UserCreateDTO(telegram_id=request_body.telegram_id)

    def get_user_update_dto(self, telegram_id: str, tags: List[str]) -> UserUpdateTagsDTO:
        return UserUpdateTagsDTO(telegram_id=telegram_id, tag_titles=tags)

    def get_event_create_dto_by_request_body(self, request_body: AddEventRequestBody) -> EventCreateDTO:
        return EventCreateDTO(
            title=request_body.title,
            description=request_body.description,
            admin_telegram_id=request_body.admin_telegram_id,
        )

    def get_event_update_dto_by_request_body(self, request_body: AddUserToEventRequestBody) -> EventUpdateUserDTO:
        return EventUpdateUserDTO(user_telegram_id=request_body.telegram_id, title=request_body.title)

    def get_all_tag_names_by_tags_dto(self, tags_dto: List[TagDTO]) -> List[str]:
        return [tag.title for tag in tags_dto]

    def get_user_telegram_ids_by_users_dto(self, users_dto: List[UserDTO]) -> List[str]:
        return [user_dto.telegram_id for user_dto in users_dto]

    def _format_base_response_header(self, models_info: List[str]) -> Dict[str, str]:
        return self._api_version | {f"model_{i}": model_info for i, model_info in enumerate(models_info, 1)}
