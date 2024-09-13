from sqlalchemy import Column, ForeignKey, Integer, String

from src.service.database_interaction.orm_models.base import Base


class RankingRequests(Base):
    __tablename__ = "ranking_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_uuid = Column(String, index=True)
    request_author_telegram_id = Column(String, ForeignKey("users.telegram_id"))
    request_result_telegram_id = Column(String, ForeignKey("users.telegram_id"))
    placement = Column(Integer)
