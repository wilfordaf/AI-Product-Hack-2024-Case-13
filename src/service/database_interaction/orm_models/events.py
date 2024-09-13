from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.service.database_interaction.orm_models.base import Base
from src.service.database_interaction.orm_models.users_events import users_events


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)

    users = relationship("Users", secondary=users_events, back_populates="events")
    admin = relationship("Users", back_populates="admin_events")
