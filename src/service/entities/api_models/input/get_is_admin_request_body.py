from pydantic import BaseModel


class GetIsAdminRequestBody(BaseModel):
    telegram_id: str
    event_title: str
