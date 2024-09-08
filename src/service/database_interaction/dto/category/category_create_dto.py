from pydantic import BaseModel


class CategoryCreateDTO(BaseModel):
    title: str
