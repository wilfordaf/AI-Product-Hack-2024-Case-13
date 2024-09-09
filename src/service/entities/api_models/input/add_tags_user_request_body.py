from pydantic import BaseModel


class AddTagsUserRequestBody(BaseModel):
    telegram_id: str
    tags: list[str]
