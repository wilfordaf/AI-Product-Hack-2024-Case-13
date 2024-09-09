from pydantic import BaseModel

from service.entities.user import User


class AddUserRequestBody(BaseModel):
    user: User
