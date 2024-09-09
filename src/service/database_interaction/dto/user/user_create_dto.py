from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    telegram_id: str
