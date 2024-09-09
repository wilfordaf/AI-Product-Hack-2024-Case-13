from pydantic import BaseModel


class AddUserRequestBody(BaseModel):
    telegram_id: str
