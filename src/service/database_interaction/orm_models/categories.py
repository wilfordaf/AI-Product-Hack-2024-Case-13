from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.service.database_interaction.orm_models.base import Base


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    tags = relationship("Tags", back_populates="category")
