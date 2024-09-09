import importlib

from service.custom_typing.endpoint_types.generic_response_type import TGenericResponse
from service.data_formatting import DataFormattingController
from service.database_interaction import DatabaseController
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

        self._logger.info("Производится настройка БД...")
        self._database_controller = DatabaseController(self._version)

        self._data_formatting_controller = DataFormattingController()

    def get_ping_response(self) -> TGenericResponse:
        models_info = [model.info for model in [self._tag_generation_model, self._ranking_model]]
        response: TGenericResponse = {
            "header": self._data_formatting_controller.format_ping_response_header(models_info),
            "body": self._data_formatting_controller.format_ping_response_body(),
        }
        self._logger.info(f"Сформирован ответ на ping: {response}")
        return response

    def get_add_user_response(self, user_id: int) -> TGenericResponse: