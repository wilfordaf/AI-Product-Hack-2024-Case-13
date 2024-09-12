import json
import os
import tempfile
from typing import Any, Dict

from linkedin_api import Linkedin
from pdfminer.high_level import extract_text

from src.service.utils.exceptions.service_error import ServiceError


def retrieve_pdf_data(text: str) -> str:
    try:
        with tempfile.TemporaryDirectory() as dirname:
            file_path = os.path.join(dirname, "tempfile.pdf")

            with open(file_path, "w") as temp_file:
                temp_file.write(text)

            with open(file_path) as temp_file:
                extracted_text: str = extract_text(temp_file)
                return extracted_text
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
    linked_username = os.getenv("LINKEDIN_USERNAME", "")
    linked_password = os.getenv("LINKEDIN_PASSWORD", "")

    try:
        api = Linkedin(linked_username, linked_password)
    except Exception as e:
        raise ServiceError(f"Ошибка при подключении к LinkedIn {e}")

    if link[-1] == "/":
        link = link[:-1]

    profile_id = link.split("/")[-1]
    profile = api.get_profile(profile_id)

    summary = profile.get("summary")
    location = profile.get("location")
    skills = profile.get("skills")
    specialty = profile.get("headline")

    if location:
        basic_location = location.get("basicLocation", {})
        country = basic_location.get("countryCode", "None").upper()
        city = basic_location.get("city", "")
        location_str = f"{city}, {country}" if city else country

    skills_str = ", ".join([skill["name"] for skill in skills]) if skills else "None"

    text = f"Summary: {summary}\n" f"Specialty: {specialty}\n" f"Location: {location_str}\n" f"Skills: {skills_str}"
    return text
