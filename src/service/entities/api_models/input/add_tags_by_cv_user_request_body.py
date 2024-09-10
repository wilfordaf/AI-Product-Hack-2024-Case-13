from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class AddTagsByCVUserRequestBody(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    telegram_id: str
    file: UploadFile
