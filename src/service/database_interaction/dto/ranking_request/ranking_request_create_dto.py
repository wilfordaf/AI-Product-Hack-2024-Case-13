from pydantic import BaseModel


class RankingRequestCreateDTO(BaseModel):
    request_uuid: str
    request_author_telegram_id: str
    request_result_telegram_id: str
    placement: int
