from pydantic import BaseModel


class SuccessStatusResponse(BaseModel):
    success: bool
