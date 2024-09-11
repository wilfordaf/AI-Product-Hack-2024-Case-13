from pydantic import BaseModel


class AddEventRequestBody(BaseModel):
    admin_telegram_id: str
    title: str
    description: str
