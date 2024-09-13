from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.service.database_interaction.orm_models.base import Base
from src.service.database_interaction.orm_models.users_tags import users_tags


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    users = relationship("Users", secondary=users_tags, back_populates="tags")
    category = relationship("Categories", back_populates="tags")
