from pydantic import BaseModel

from service.entities.user import User


class GetRankingUserRequestBody(BaseModel):
    user: User
