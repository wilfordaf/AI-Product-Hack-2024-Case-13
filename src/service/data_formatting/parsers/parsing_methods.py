import json
import os
import tempfile
from typing import Any, Dict

from pdfminer.high_level import extract_text

from src.service.utils.exceptions.service_error import ServiceError


def retrieve_pdf_data(text: str) -> str:
    try:
        with tempfile.TemporaryDirectory() as dirname:
            file_path = os.path.join(dirname, "tempfile.txt")

            with open(file_path, "w") as temp_file:
                temp_file.write(text)

            with open(file_path) as temp_file:
                return extract_text(temp_file)
    except Exception as e:
        raise ServiceError(f"При чтении pdf файла возникла ошибка: {str(e)}") from e


def retrieve_json_data(text: str, from_id: str) -> str:
    n_messages = 200
    try:
        content: Dict[str, Any] = json.loads(text)
        return "\n".join(
            [
                message["text"]
                for message in filter(
                    lambda m: m["from_id"] == from_id,
                    content["messages"],
                )
            ][-n_messages:]
        )
    except Exception as e:
        raise ServiceError(f"При чтении json файла возникла ошибка: {str(e)}") from e


def retrieve_linkedin_data(link: str) -> str:
    raise NotImplementedError("Функция не реализована")
