from typing import List

from pydantic import BaseModel, ConfigDict


class UserUpdateTagsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: str
    tag_titles: List[str]
