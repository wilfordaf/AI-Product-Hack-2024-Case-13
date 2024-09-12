from typing import List, TypedDict

from src.service.custom_typing import TUser


class TUserRankingResponseBody(TypedDict):
    users: List[TUser]
