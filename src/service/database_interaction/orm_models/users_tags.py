from sqlalchemy import Column, ForeignKey, Integer, Table

from src.service.database_interaction.orm_models.base import Base

users_tags = Table(
    "users_tags",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
