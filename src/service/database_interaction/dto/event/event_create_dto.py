from pydantic import BaseModel


class EventCreateDTO(BaseModel):
    title: str
    description: str
    admin_id: int
