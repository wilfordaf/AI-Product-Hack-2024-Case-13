from pydantic import BaseModel


class GetRankingUserRequestBody(BaseModel):
    telegram_id: str
    event_title: str
