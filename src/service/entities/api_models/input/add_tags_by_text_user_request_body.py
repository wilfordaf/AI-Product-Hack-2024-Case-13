from pydantic import BaseModel


class AddTagsByTextUserRequestBody(BaseModel):
    telegram_id: str
    text: str
