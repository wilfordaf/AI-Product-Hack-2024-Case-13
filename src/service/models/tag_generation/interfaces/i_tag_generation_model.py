from abc import ABC, abstractmethod
from typing import List

from service.custom_typing import TModelInfo


class ITagGenerationModel(ABC):
    @property
    @abstractmethod
    def info(self) -> TModelInfo:
        """
        Returns information about the model, including its name and version.
        :return: Information about the model as a dictionary with keys 'name' and 'version'.
        """

    @abstractmethod
    def load_model(self) -> None:
        """
        Loads the model from disk or other storage. This method is called before generating tags.
        """

    @abstractmethod
    def generate_tags(self, text: str) -> List[str]:
        """
        Generate tags for the given text. The function should return a list of strings representing the generated tags.
        :param text: Input text to generate tags from.
        :return: List of generated tags.
        """
