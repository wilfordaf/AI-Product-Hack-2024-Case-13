from pathlib import Path
from typing import Any, Dict

from src.service.utils.file_parsers.file_parser import FileParser


class SQLFileParser(FileParser):
    _EXTENSION = ".sql"

    def __init__(self, filepath: Path, **kwargs):
        super().__init__(filepath)
        self._query_parameters = kwargs

    def _parse_file(self) -> Dict[str, Any]:
        with open(self._filepath, encoding="utf-8") as fin:
            query = fin.read()
            formatted_query = query.format(**self._query_parameters)
            data: Dict[str, Any] = {"query": formatted_query}
            return data
