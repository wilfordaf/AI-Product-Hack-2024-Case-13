from pydantic import BaseModel


class TagCreateDTO(BaseModel):
    title: str
    category_id: int
