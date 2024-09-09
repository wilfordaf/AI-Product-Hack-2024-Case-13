import importlib

from service.custom_typing.endpoint_types.generic_response_type import TGenericResponse
from service.data_formatting import DataFormattingController
from service.database_interaction import DatabaseController
from service.entities.api_models.input import AddUserRequestBody
from service.entities.api_models.input.add_tags_user_request_body import (
    AddTagsUserRequestBody,
)
from service.models.ranking import CosineRankingModel
from service.models.tag_generation import OllamaGenerationModel
from service.utils.exceptions import ServiceError
from service.utils.logging import ConsoleLogger


class ServiceAssembler:
    def __init__(self):
        try:
            self._version = getattr(importlib.import_module(".".join(self.__module__.split(".")[:-1])), "version")
        except ModuleNotFoundError as e:
            raise ServiceError("В модуле сервиса отсутствует version.py или она не указана в __init__.py") from e

        self._logger = ConsoleLogger()
        self._logger.info("Производится запуск сервиса...")

        self._tag_generation_model = OllamaGenerationModel()
        self._tag_generation_model.load_model()

        self._ranking_model = CosineRankingModel()
        self._ranking_model.load_model()

        self._models = [model.info for model in [self._tag_generation_model, self._ranking_model]]

        self._logger.info("Производится настройка БД...")
        self._database_controller = DatabaseController()

        self._data_formatting_controller = DataFormattingController(self._version)

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

    def get_add_tags_to_user_response(self, request_body: AddTagsUserRequestBody) -> TGenericResponse:
        user_update_dto = self._data_formatting_controller.get_user_update_dto_by_request_body(request_body)
        tags_names = [tag.title for tag in self._database_controller.get_all_tags()]

        tags_to_add = [tag for tag in user_update_dto.tags if tag in tags_names]
        user_update_dto.tag_titles = tags_to_add
        try:
            self._database_controller.update_user_tags(user_update_dto)
            success = True
        except ServiceError:
            success = False

        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_add_tags_to_user_response_header(self._models),
            "body": self._data_formatting_controller.format_add_tags_to_user_response_body(success),
        }
        self._logger.info(f"Formatted /user/add-tags response: {response}")
        return response
