from typing import List, Optional

from sqlalchemy.orm import Session

from src.service.database_interaction.dto.tag import TagCreateDTO, TagDTO
from src.service.database_interaction.orm_models.tags import Tags


class TagRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, tag_create_dto: TagCreateDTO) -> None:
        tag = Tags(title=tag_create_dto.title, category_id=tag_create_dto.category_id)
        self._session.add(tag)
        self._session.commit()
        self._session.refresh(tag)

    def read_by_title(self, title: str) -> Optional[TagDTO]:
        tag = self._session.query(Tags).filter(Tags.title == title).first()
        return TagDTO.model_validate(tag) if tag else None

    def delete(self, tag_id: int):
        tag = self._session.query(Tags).filter(Tags.id == tag_id).first()
        if not tag:
            return

        self._session.delete(tag)
        self._session.commit()

    def get_all_tags(self) -> List[TagDTO]:
        tags = self._session.query(Tags).all()
        return [TagDTO.model_validate(tag) for tag in tags]
