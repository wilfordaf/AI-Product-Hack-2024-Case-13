from typing import Optional

from sqlalchemy.orm import Session, sessionmaker

from src.service.database_interaction.dto.category import CategoryCreateDTO, CategoryDTO
from src.service.database_interaction.orm_models.categories import Categories


class CategoryRepository:
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def create(self, category_create_dto: CategoryCreateDTO) -> None:
        with self._session_maker() as session:
            category = Categories(title=category_create_dto.title)
            session.add(category)
            session.commit()
            session.refresh(category)

    def read_by_name(self, title: str) -> Optional[CategoryDTO]:
        with self._session_maker() as session:
            category = session.query(Categories).filter(Categories.title == title).first()
            return CategoryDTO.model_validate(category) if category else None

    def delete(self, category_id: int):
        with self._session_maker() as session:
            category = session.query(Categories).filter(Categories.id == category_id).first()
            if not category:
                return

            session.delete(category)
            session.commit()
