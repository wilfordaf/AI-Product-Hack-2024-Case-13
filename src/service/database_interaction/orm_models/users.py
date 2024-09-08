from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.service.database_interaction.orm_models.base import Base
from src.service.database_interaction.orm_models.users_events import users_events
from src.service.database_interaction.orm_models.users_tags import users_tags


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)

    events = relationship("Events", secondary=users_events, back_populates="users")
    tags = relationship("Tags", secondary=users_tags, back_populates="users")
