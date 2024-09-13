from pydantic import BaseModel, ConfigDict


class EventDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    admin_id: int
    title: str
    description: str
