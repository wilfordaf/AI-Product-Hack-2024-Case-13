from typing import List, Optional

from sqlalchemy.orm import Session, sessionmaker

from src.service.database_interaction.dto.user import (
    UserCreateDTO,
    UserDTO,
    UserUpdateTagsDTO,
)
from src.service.database_interaction.orm_models.tags import Tags
from src.service.database_interaction.orm_models.users import Users


class UserRepository:
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def create(self, user_create_dto: UserCreateDTO) -> None:
        with self._session_maker() as session:
            user = Users(telegram_id=user_create_dto.telegram_id)
            session.add(user)
            session.commit()
            session.refresh(user)

    def read_by_telegram_id(self, telegram_id: str) -> Optional[UserDTO]:
        with self._session_maker() as session:
            user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
            if not user:
                return None

            return UserDTO.model_validate(
                {
                    "id": user.id,
                    "telegram_id": user.telegram_id,
                    "tags": [tag.title for tag in user.tags],
                }
            )

    def delete(self, user_id: int):
        with self._session_maker() as session:
            user = session.query(Users).filter(Users.id == user_id).first()
            if not user:
                return

            session.delete(user)
            session.commit()

    def add_tags_to_user(self, user_update_dto: UserUpdateTagsDTO) -> None:
        with self._session_maker() as session:
            user = session.query(Users).filter(Users.telegram_id == user_update_dto.telegram_id).first()
            if not user:
                return

            tags = session.query(Tags).filter(Tags.title.in_(user_update_dto.tag_titles)).all()
            for tag in tags:
                user.tags.append(tag)

            session.commit()

    def get_users_by_telegram_ids(self, telegram_ids: List[str]) -> List[UserDTO]:
        with self._session_maker() as session:
            users = session.query(Users).filter(Users.telegram_id.in_(telegram_ids)).all()

            users_dto = []
            for user in users:
                tag_titles = [tag.title for tag in user.tags]
                user_dto = UserDTO.model_validate(
                    {
                        "id": user.id,
                        "telegram_id": user.telegram_id,
                        "tags": tag_titles,
                    }
                )
                users_dto.append(user_dto)

            return users_dto
