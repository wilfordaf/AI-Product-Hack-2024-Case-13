import importlib
from typing import List, Tuple

from src.service.models.ranking.interfaces import IRankingModel
from src.service.utils.exceptions import ServiceError
from src.service.utils.logging import ConsoleLogger


class CosineRankingModel(IRankingModel):
    def __init__(self, possible_tags: List[str]):
        try:
            self._version = getattr(importlib.import_module(".".join(self.__module__.split(".")[:-1])), "version")
        except AttributeError as e:
            raise ServiceError("Module does not have version.py or it is not in __init__.py") from e
        except ValueError as e:
            raise ServiceError(f"Incorrect path to {self.__module__}") from e

        self._possible_tags = possible_tags
        self._logger = ConsoleLogger()

    @property
    def info(self) -> str:
        return f"CosineRankingModel v{self._version}"

    def load_model(self) -> None:
        pass

    def perform_ranking(self, caller_telegram_id: str, n: int) -> List[Tuple[str, List[str]]]:
        raise NotImplementedError("This method is not implemented in this class")
