from pydantic import BaseModel, ConfigDict


class RankingRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_uuid: str
    request_author_telegram_id: str
    request_result_telegram_id: str
    placement: int
