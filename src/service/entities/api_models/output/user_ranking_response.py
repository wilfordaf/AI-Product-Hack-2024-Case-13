from typing import List

from pydantic import BaseModel

from src.service.entities.user import User


class UserRankingResponse(BaseModel):
    users: List[User]
