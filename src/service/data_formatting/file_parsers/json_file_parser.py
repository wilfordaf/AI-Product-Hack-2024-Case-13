import json
from typing import Any, Dict

from src.service.data_formatting.file_parsers.file_parser import FileParser


class JsonFileParser(FileParser):
    _EXTENSION = ".json"

    def _parse_file(self) -> str:
        with open(self._filepath, encoding="utf-8") as fin:
            content: Dict[str, Any] = json.load(fin)

            text = ""
            for message in content['messages']:
                text += message['text'] + " "

            return text
