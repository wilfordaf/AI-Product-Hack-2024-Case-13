from pydantic import BaseModel, ConfigDict


class TagDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category_id: int
