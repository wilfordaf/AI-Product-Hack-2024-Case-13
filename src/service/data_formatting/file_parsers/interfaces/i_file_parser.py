from abc import ABC, abstractmethod


class IFileParser(ABC):
    @abstractmethod
    def retrieve_data(self) -> str:
        """
        Retrieves data from a file and returns it as a string.
        :return: The content of the file as a string.
        """
