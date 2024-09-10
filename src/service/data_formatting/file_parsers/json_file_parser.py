import json
from typing import Any, Dict

from src.service.data_formatting.file_parsers.file_parser import FileParser
from src.service.utils.exceptions import ServiceError


class JsonFileParser(FileParser):
    _EXTENSION = ".json"

    def retrieve_data(self, from_id: str) -> str:
        try:
            return self._parse_file(from_id)
        except Exception as e:
            raise ServiceError(f"При чтении файла {self._filepath} возникла ошибка: {str(e)}") from e

    def _parse_file(self, from_id: str) -> str:
        with open(self._filepath, encoding="utf-8") as fin:
            content: Dict[str, Any] = json.load(fin)

            return "\n".join([message for message in content['message'] if message['from_id'] == from_id])

