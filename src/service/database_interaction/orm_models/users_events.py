from sqlalchemy import Column, ForeignKey, Integer, Table

from src.service.database_interaction.orm_models.base import Base

users_events = Table(
    "users_events",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)
