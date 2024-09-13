from pydantic import BaseModel


class GetUsersByEventRequestBody(BaseModel):
    event_title: str
