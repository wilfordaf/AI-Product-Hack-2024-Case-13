from abc import ABC, abstractmethod
from typing import List, Tuple


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
    def save_model(self) -> None:
        """
        Saves the model to disk.
        """

    @abstractmethod
    def add_user(self, telegram_id: str, tags: List[str]) -> None:
        """
        Adds a user with his tags vector. This method is called before generating tags.
        :param telegram_id: Telegram id of the user.
        :param tags: User's tags.
        """

    @abstractmethod
    def perform_ranking(self, caller_telegram_id: str, event_user_ids, n: int) -> List[Tuple[str, List[str]]]:
        """
        Performs the ranking of users based on tags vectors.
        :param caller_telegram_id: Telegram id of the user who called the method.
        :param event_user_ids: List of telegram ids of users who participated in the event.
        :param n: Number of users to return in the ranking.
        :return: Ordered tuples of (telegram_id, [matching_tags]).
        """
