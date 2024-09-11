from pydantic import BaseModel, ConfigDict


class EventUpdateUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    user_telegram_id: str
