import os
from typing import Any, Callable, List

from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker

from src.service.database_interaction.dto.tag.tag_dto import TagDTO
from src.service.database_interaction.dto.user import UserCreateDTO, UserUpdateTagsDTO
from src.service.database_interaction.dto.user.user_dto import UserDTO
from src.service.database_interaction.orm_models.base import Base
from src.service.database_interaction.repositories import (
    CategoryRepository,
    EventRepository,
    RankingRequestRepository,
    TagRepository,
    UserRepository,
)
from src.service.utils.exceptions import ServiceError
from src.service.utils.logging import ConsoleLogger


class DatabaseController:
    _CONNECTION_STRING_VAR_NAME = "DATABASE_URL"

    def __init__(self):
        raw_connection_string = os.getenv(self._CONNECTION_STRING_VAR_NAME, "")
        self._logger = ConsoleLogger()
        try:
            connection_url = make_url(raw_connection_string)
            engine = create_engine(connection_url)
            Base.metadata.create_all(bind=engine)

            self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        except Exception as e:
            self._logger.critical(f"Failed to connect to database: {e}")
            raise ServiceError("Connection to DB Failed")

        self._user_repository = UserRepository(self._session_maker)
        self._category_repository = CategoryRepository(self._session_maker)
        self._tag_repository = TagRepository(self._session_maker)
        self._event_repository = EventRepository(self._session_maker)
        self._ranking_request_repository = RankingRequestRepository(self._session_maker)

    def add_user(self, user: UserCreateDTO) -> None:
        self._execute_repository_method(self._user_repository.create, user_create_dto=user)

    def update_user_tags(self, user_update_tags_dto: UserUpdateTagsDTO) -> None:
        self._execute_repository_method(
            self._user_repository.add_tags_to_user,
            user_update_dto=user_update_tags_dto,
        )

    def is_admin(self, user_telegram_id: str, event_title: str) -> bool:
        is_admin: bool = self._execute_repository_method(
            self._event_repository.is_admin,
            telegram_id=user_telegram_id,
            event_title=event_title,
        )
        return is_admin

    def get_all_tags(self) -> List[TagDTO]:
        all_tags: List[TagDTO] = self._execute_repository_method(self._tag_repository.get_all_tags)
        return all_tags

    def get_users_by_telegram_ids(self, telegram_ids: List[str]) -> List[UserDTO]:
        users: List[UserDTO] = self._execute_repository_method(
            self._user_repository.get_users_by_telegram_ids,
            telegram_i=telegram_ids,
        )
        return users

    def _execute_repository_method(self, method: Callable[..., Any], **kwargs) -> Any:
        try:
            result = method(**kwargs)
            self._logger.debug(f"{method.__name__} with {kwargs} executed successfully")
            return result
        except Exception as e:
            msg = f"Failed to execute {method.__name__}: {e}"
            self._logger.error(msg)
            raise ServiceError(msg)
