from typing import List

from pydantic import BaseModel

from service.entities.user import User


class UserRankingResponse(BaseModel):
    ranking_result: List[User]
