import os
from pathlib import Path
from typing import Any, Callable, List

from sqlalchemy import create_engine, make_url, text
from sqlalchemy.orm import sessionmaker

from src.service.database_interaction.dto.event import (
    EventCreateDTO,
    EventUpdateUserDTO,
)
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
    _SQL_SCRIPTS_DIR = Path(__file__).parents[3] / "sql"

    def __init__(self):
        raw_connection_string = os.getenv(self._CONNECTION_STRING_VAR_NAME, "")
        self._logger = ConsoleLogger()
        try:
            connection_url = make_url(raw_connection_string)
            self._engine = create_engine(connection_url)
            Base.metadata.create_all(bind=self._engine)
            self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        except Exception as e:
            self._logger.critical(f"Failed to connect to database: {e}")
            raise ServiceError("Connection to DB Failed")

        self._user_repository = UserRepository(self._session_maker)
        self._category_repository = CategoryRepository(self._session_maker)
        self._tag_repository = TagRepository(self._session_maker)
        self._event_repository = EventRepository(self._session_maker)
        self._ranking_request_repository = RankingRequestRepository(self._session_maker)

        # TODO: Remove in production
        self._execute_example_startup_script()

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
            user_telegram_id=user_telegram_id,
            event_title=event_title,
        )
        return is_admin

    def get_all_tags(self) -> List[TagDTO]:
        all_tags: List[TagDTO] = self._execute_repository_method(self._tag_repository.get_all_tags)
        return all_tags

    def get_tags_by_user(self, telegram_id: str) -> List[TagDTO]:
        all_tags: List[TagDTO] = self._execute_repository_method(
            self._tag_repository.get_tags_by_user_telegram_id,
            telegram_id=telegram_id,
        )
        return all_tags

    def get_users_by_telegram_ids(self, telegram_ids: List[str]) -> List[UserDTO]:
        users: List[UserDTO] = self._execute_repository_method(
            self._user_repository.get_users_by_telegram_ids,
            telegram_ids=telegram_ids,
        )
        return users

    def get_users_by_event_title(self, event_title: str) -> List[UserDTO]:
        users: List[UserDTO] = self._execute_repository_method(
            self._event_repository.get_users_by_event_title,
            event_title=event_title,
        )
        return users

    def add_event(self, event: EventCreateDTO) -> None:
        self._execute_repository_method(self._event_repository.create, event_create_dto=event)

    def add_user_to_event(self, event_update_user_dto: EventUpdateUserDTO) -> None:
        self._execute_repository_method(
            self._event_repository.add_user_to_event,
            event_update_user_dto=event_update_user_dto,
        )

    def _execute_example_startup_script(self) -> None:
        if self.get_all_tags():
            return

        script_path = self._SQL_SCRIPTS_DIR / "example_startup.sql"
        self._execute_sql_script(script_path)

    def _execute_sql_script(self, script_path: Path) -> None:
        if not script_path.exists():
            self._logger.error(f"SQL script file '{script_path}' not found.")
            raise ServiceError(f"SQL script file '{script_path}' not found.")

        try:
            with open(script_path) as file:
                sql_script = file.read()

            with self._engine.connect() as connection:
                connection.execute(text(sql_script))
                connection.commit()

            self._logger.info(f"SQL script '{script_path}' executed successfully.")
        except Exception as e:
            self._logger.error(f"Failed to execute SQL script '{script_path}': {e}")
            raise ServiceError(f"Failed to execute SQL script '{script_path}'")

    def _execute_repository_method(self, method: Callable[..., Any], **kwargs) -> Any:
        try:
            result = method(**kwargs)
            self._logger.debug(f"{method.__name__} with {kwargs} executed successfully")
            return result
        except Exception as e:
            msg = f"Failed to execute {method.__name__}: {e}"
            self._logger.error(msg)
            raise ServiceError(msg)
