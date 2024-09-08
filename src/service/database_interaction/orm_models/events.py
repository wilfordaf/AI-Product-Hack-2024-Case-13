from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.service.database_interaction.orm_models.base import Base
from src.service.database_interaction.orm_models.users_events import users_events


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    users = relationship("Users", secondary=users_events, back_populates="events")
