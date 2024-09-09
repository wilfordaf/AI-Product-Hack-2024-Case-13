from typing import List

from pydantic import BaseModel


class User(BaseModel):
    telegram_id: str
    tags: List[str]
