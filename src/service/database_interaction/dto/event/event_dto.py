from pydantic import BaseModel, ConfigDict


class EventDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
