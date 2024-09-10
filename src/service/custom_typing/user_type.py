from typing import List, TypedDict


class TUser(TypedDict):
    telegram_id: str
    tags: List[str]
