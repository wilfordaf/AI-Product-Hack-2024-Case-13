from pydantic import BaseModel


class GetTagsByUserRequestBody(BaseModel):
    telegram_id: str
