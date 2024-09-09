from pydantic import BaseModel

from service.entities.user import User


class AddTagsUserRequestBody(BaseModel):
    user: User
    tags: list[str]
