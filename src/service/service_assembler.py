import importlib
from typing import List

from src.service.custom_typing.endpoint_types import TGenericResponse
from src.service.data_formatting import DataFormattingController
from src.service.data_formatting.parsers.parsing_methods import (
    retrieve_json_data,
    retrieve_linkedin_data,
    retrieve_pdf_data,
)
from src.service.database_interaction import DatabaseController
from src.service.entities.api_models.input import (
    AddTagsByLinkUserRequestBody,
    AddTagsByTextUserRequestBody,
    AddUserRequestBody,
    AddUserToEventRequestBody,
    GetIsAdminRequestBody,
    GetRankingUserRequestBody,
    GetTagsByUserRequestBody,
    GetUsersByEventRequestBody,
)
from src.service.entities.api_models.input.add_event_request_body import (
    AddEventRequestBody,
)
from src.service.models.ranking import CosineRankingModel
from src.service.models.tag_generation import OllamaGenerationModel
from src.service.utils.exceptions import ServiceError
from src.service.utils.logging import ConsoleLogger


class ServiceAssembler:
    _RANKING_TOP_N = 5

    def __init__(self):
        try:
            self._version = getattr(importlib.import_module(".".join(self.__module__.split(".")[:-1])), "version")
        except ModuleNotFoundError as e:
            raise ServiceError("В модуле сервиса отсутствует version.py или она не указана в __init__.py") from e

        self._logger = ConsoleLogger()
        self._logger.info("Производится запуск сервиса...")
        self._data_formatting_controller = DataFormattingController(self._version)

        self._logger.info("Производится настройка БД...")
        self._database_controller = DatabaseController()
        all_tags = self._database_controller.get_all_tags()
        tag_names = self._data_formatting_controller.get_all_tag_names_by_tags_dto(all_tags)

        self._logger.info("Производится загрузка моделей")
        self._tag_generation_model = OllamaGenerationModel(tag_names)
        self._tag_generation_model.load_model()

        self._ranking_model = CosineRankingModel(tag_names)
        self._ranking_model.load_model()

        self._models = [model.info for model in [self._tag_generation_model, self._ranking_model]]  # type: ignore

    def get_ping_response(self) -> TGenericResponse:
        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_ping_response_header(self._models),
            "body": self._data_formatting_controller.format_ping_response_body(),
        }
        self._logger.info(f"Formatted /ping response: {response}")
        return response

    def get_add_user_response(self, request_body: AddUserRequestBody) -> TGenericResponse:
        user_create_dto = self._data_formatting_controller.get_user_create_dto_by_request_body(request_body)
        try:
            self._database_controller.add_user(user_create_dto)
            success = True
        except ServiceError:
            success = False

        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_add_user_response_header(self._models),
            "body": self._data_formatting_controller.format_add_user_response_body(success),
        }
        self._logger.info(f"Formatted /user/add response: {response}")
        return response

    def get_add_tags_by_text_to_user_response(
        self,
        request_body: AddTagsByTextUserRequestBody,
    ) -> TGenericResponse:
        generated_tags = self._tag_generation_model.generate_tags(request_body.text)
        response = self._add_tags_to_user(request_body.telegram_id, generated_tags)
        self._logger.info(f"Formatted /user/add-tags/text response: {response}")
        return response

    def get_add_tags_by_link_to_user_response(
        self,
        request_body: AddTagsByLinkUserRequestBody,
    ) -> TGenericResponse:
        generated_tags = self._tag_generation_model.generate_tags(retrieve_linkedin_data(request_body.link))
        response = self._add_tags_to_user(request_body.telegram_id, generated_tags)
        self._logger.info(f"Formatted /user/add-tags/link response: {response}")
        return response

    def get_add_tags_by_cv_to_user_response(
        self,
        request_body: AddTagsByTextUserRequestBody,
    ) -> TGenericResponse:
        generated_tags = self._tag_generation_model.generate_tags(retrieve_pdf_data(request_body.text))
        response = self._add_tags_to_user(request_body.telegram_id, generated_tags)
        self._logger.info(f"Formatted /user/add-tags/cv response: {response}")
        return response

    def get_add_tags_by_dialogue_to_user_response(
        self,
        request_body: AddTagsByTextUserRequestBody,
    ) -> TGenericResponse:
        generated_tags = self._tag_generation_model.generate_tags(
            retrieve_json_data(
                request_body.text,
                request_body.telegram_id,
            )
        )
        response = self._add_tags_to_user(request_body.telegram_id, generated_tags)
        self._logger.info(f"Formatted /user/add-tags/dialogue response: {response}")
        return response

    def get_user_ranking_response(self, request_body: GetRankingUserRequestBody) -> TGenericResponse:
        event_users = self._database_controller.get_users_by_event_title(request_body.event_title)
        ranked_user_telegram_ids = self._ranking_model.perform_ranking(request_body.telegram_id, event_users, 5)
        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_get_ranking_user_response_header(self._models),
            "body": self._data_formatting_controller.format_get_ranking_user_response_body(ranked_user_telegram_ids),
        }
        self._logger.info(f"Formatted /user/get-ranking response: {response}")
        return response

    def get_is_admin_response(self, request_body: GetIsAdminRequestBody) -> TGenericResponse:
        is_admin = self._database_controller.is_admin(request_body.telegram_id, request_body.event_title)
        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_get_is_admin_response_header(self._models),
            "body": self._data_formatting_controller.format_get_is_admin_response_body(is_admin),
        }
        self._logger.info(f"Formatted /user/get-ranking response: {response}")
        return response

    def get_users_by_event_response(self, request_body: GetUsersByEventRequestBody) -> TGenericResponse:
        event_users = self._database_controller.get_users_by_event_title(request_body.event_title)
        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_get_event_users_response_header(self._models),
            "body": self._data_formatting_controller.format_get_event_users_response_body(event_users),
        }
        self._logger.info(f"Formatted /event/get-users response: {response}")
        return response

    def get_tags_by_user_response(self, request_body: GetTagsByUserRequestBody) -> TGenericResponse:
        tags = self._database_controller.get_tags_by_user(request_body.telegram_id)
        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_get_tags_by_user_response_header(self._models),
            "body": self._data_formatting_controller.format_get_tags_by_user_response_body(tags),
        }
        self._logger.info(f"Formatted /user/get-tags response: {response}")
        return response

    def get_add_event_response(self, request_body: AddEventRequestBody) -> TGenericResponse:
        event_create_dto = self._data_formatting_controller.get_event_create_dto_by_request_body(request_body)
        try:
            self._database_controller.add_event(event_create_dto)
            success = True
        except ServiceError:
            success = False

        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_add_event_response_header(self._models),
            "body": self._data_formatting_controller.format_add_event_response_body(success),
        }
        self._logger.info(f"Formatted /event/add response: {response}")
        return response

    def get_add_user_to_event_response(self, request_body: AddUserToEventRequestBody) -> TGenericResponse:
        event_update_dto = self._data_formatting_controller.get_event_update_dto_by_request_body(request_body)
        try:
            self._database_controller.add_user_to_event(event_update_dto)
            success = True
        except ServiceError:
            success = False

        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_add_user_to_event_response_header(self._models),
            "body": self._data_formatting_controller.format_add_user_to_event_response_body(success),
        }
        self._logger.info(f"Formatted /event/add-user response: {response}")
        return response

    def _add_tags_to_user(self, telegram_id: str, tags: List[str]) -> TGenericResponse:
        user_update_dto = self._data_formatting_controller.get_user_update_dto(telegram_id, tags)
        tags_names = [tag.title for tag in self._database_controller.get_all_tags()]

        tags_to_add = [tag for tag in user_update_dto.tag_titles if tag in tags_names]
        user_update_dto.tag_titles = tags_to_add
        try:
            self._database_controller.update_user_tags(user_update_dto)
            self._ranking_model.add_user(telegram_id, tags_to_add)
            success = True
        except ServiceError:
            success = False

        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_add_tags_to_user_response_header(self._models),
            "body": self._data_formatting_controller.format_add_tags_to_user_response_body(success),
        }
        return response
