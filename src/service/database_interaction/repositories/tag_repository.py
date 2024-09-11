from typing import List, Optional

from sqlalchemy.orm import Session, sessionmaker

from src.service.database_interaction.dto.tag import TagCreateDTO, TagDTO
from src.service.database_interaction.orm_models.tags import Tags
from src.service.database_interaction.orm_models.users import Users


class TagRepository:
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def create(self, tag_create_dto: TagCreateDTO) -> None:
        with self._session_maker() as session:
            tag = Tags(title=tag_create_dto.title, category_id=tag_create_dto.category_id)
            session.add(tag)
            session.commit()
            session.refresh(tag)

    def read_by_title(self, title: str) -> Optional[TagDTO]:
        with self._session_maker() as session:
            tag = session.query(Tags).filter(Tags.title == title).first()
            return TagDTO.model_validate(tag) if tag else None

    def delete(self, tag_id: int):
        with self._session_maker() as session:
            tag = session.query(Tags).filter(Tags.id == tag_id).first()
            if not tag:
                return

            session.delete(tag)
            session.commit()

    def get_all_tags(self) -> List[TagDTO]:
        with self._session_maker() as session:
            tags = session.query(Tags).all()
            return [TagDTO.model_validate(tag) for tag in tags]

    def get_tags_by_user_telegram_id(self, telegram_id: str) -> List[TagDTO]:
        with self._session_maker() as session:
            user = session.query(Users).filter(Users.telegram_id == telegram_id).first()

            if not user:
                return []

            tags = user.tags
            return [TagDTO.model_validate(tag) for tag in tags]
