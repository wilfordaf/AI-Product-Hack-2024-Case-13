from typing import List, Optional

from sqlalchemy.orm import Session

from src.service.database_interaction.dto.user import UserCreateDTO, UserDTO
from src.service.database_interaction.orm_models.tags import Tags
from src.service.database_interaction.orm_models.users import Users


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, user_create_dto: UserCreateDTO) -> None:
        user = Users(telegram_id=user_create_dto.telegram_id)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

    def read_by_telegram_id(self, telegram_id: str) -> Optional[UserDTO]:
        user = self._session.query(Users).filter(Users.telegram_id == telegram_id).first()
        return UserDTO.model_validate(user) if user else None

    def delete(self, user_id: int):
        user = self._session.query(Users).filter(Users.id == user_id).first()
        if not user:
            return

        self._session.delete(user)
        self._session.commit()

    def add_tags_to_user(self, user_id: int, tag_ids: List[int]) -> None:
        user = self._session.query(Users).filter(Users.id == user_id).first()
        if not user:
            return

        tags = self._session.query(Tags).filter(Tags.id.in_(tag_ids)).all()
        for tag in tags:
            user.tags.append(tag)

        self._session.commit()
