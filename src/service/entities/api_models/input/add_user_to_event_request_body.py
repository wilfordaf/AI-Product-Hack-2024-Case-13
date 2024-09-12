from pydantic import BaseModel


class AddUserToEventRequestBody(BaseModel):
    telegram_id: str
    title: str
