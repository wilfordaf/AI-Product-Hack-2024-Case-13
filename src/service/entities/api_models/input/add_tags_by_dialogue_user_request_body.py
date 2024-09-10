from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class AddTagsByDialogueUserRequestBody(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    telegram_id: str
    file: UploadFile
