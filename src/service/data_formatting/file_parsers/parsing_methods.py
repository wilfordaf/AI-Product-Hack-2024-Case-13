import json
import os
from pathlib import Path
from typing import Any, Dict

from pdfminer.high_level import extract_text

from service.utils.exceptions.service_error import ServiceError


def retrieve_pdf_data(filepath: Path) -> str:
    extension = ".pdf"
    raise_invalid_retrieve_data(filepath, extension)

    try:
        with open(filepath, mode="rb") as fin:
            return extract_text(fin)
    except Exception as e:
        raise ServiceError(f"При чтении файла {filepath} возникла ошибка: {str(e)}") from e


def retrieve_json_data(filepath: Path, from_id: int) -> str:
    extension = ".json"
    n_messages = 200
    raise_invalid_retrieve_data(filepath, extension)

    try:
        with open(filepath, encoding="utf-8") as fin:
            content: Dict[str, Any] = json.load(fin)
            return "\n".join(
                [message["text"] for message in content["messages"][-n_messages:] if message["from_id"] == from_id]
            )
    except Exception as e:
        raise ServiceError(f"При чтении файла {filepath} возникла ошибка: {str(e)}") from e


def raise_invalid_retrieve_data(filepath: Path, extension: str) -> str:
    if filepath.suffix != extension:
        raise ServiceError(f"Расширение {filepath.suffix} не является {extension}")

    if not os.path.exists(filepath):
        raise ServiceError(f"Файл по пути {filepath.resolve()} не найден")
