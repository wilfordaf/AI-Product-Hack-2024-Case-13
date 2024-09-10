from pydantic import BaseModel


class AddTagsByLinkUserRequestBody(BaseModel):
    telegram_id: str
    link: str
