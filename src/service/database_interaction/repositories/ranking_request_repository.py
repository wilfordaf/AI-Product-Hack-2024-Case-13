from typing import Optional

from sqlalchemy.orm import Session

from src.service.database_interaction.dto.ranking_request import (
    RankingRequestCreateDTO,
    RankingRequestDTO,
)
from src.service.database_interaction.orm_models.ranking_requests import RankingRequests


class RankingRequestRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, ranking_request_create_dto: RankingRequestCreateDTO) -> None:
        ranking_request = RankingRequests(
            request_uuid=ranking_request_create_dto.request_uuid,
            request_author_telegram_id=ranking_request_create_dto.request_author_telegram_id,
            request_result_telegram_id=ranking_request_create_dto.request_result_telegram_id,
            placement=ranking_request_create_dto.placement,
        )
        self._session.add(ranking_request)
        self._session.commit()
        self._session.refresh(ranking_request)

    def read_by_uuid(self, request_uuid: str) -> Optional[RankingRequestDTO]:
        ranking_request = (
            self._session.query(RankingRequests).filter(RankingRequests.request_uuid == request_uuid).first()
        )
        return RankingRequestDTO.model_validate(ranking_request) if ranking_request else None

    def delete(self, request_id: int):
        ranking_request = self._session.query(RankingRequests).filter(RankingRequests.id == request_id).first()
        if not ranking_request:
            return

        self._session.delete(ranking_request)
        self._session.commit()
