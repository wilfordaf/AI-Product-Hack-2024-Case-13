from abc import ABC, abstractmethod
from typing import List


class IRankingModel(ABC):
    @property
    @abstractmethod
    def info(self) -> str:
        """
        Returns a string with information about the ranking model
        :return: String with information about the ranking model
        """

    @abstractmethod
    def load_model(self) -> None:
        """
        Loads the model from disk or other storage. This method is called before generating tags.
        """

    @abstractmethod
    def perform_ranking(self, caller_telegram_id: str, n: int) -> List[str]:
        """
        Performs the ranking of users based on tags vectors.
        The method returns a sorted list of top-n telegram ids.
        :param caller_telegram_id: Telegram id of the user who called the method.
        :param n: Number of users to return in the ranking.
        :return: Sorted list of top-n telegram ids.
        """
