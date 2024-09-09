import os

from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker

from service.database_interaction.repositories import (
    CategoryRepository,
    EventRepository,
    RankingRequestRepository,
    TagRepository,
    UserRepository,
)
from service.utils.exceptions import ServiceError
from service.utils.logging import ConsoleLogger
from src.service.database_interaction.orm_models.base import Base


class DatabaseController:
    _CONNECTION_STRING_VAR_NAME = "DATABASE_URL"

    def __init__(self):
        raw_connection_string = os.getenv(self._CONNECTION_STRING_VAR_NAME, "")
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

        self._logger = ConsoleLogger()

    # TODO: верхнеуровневые методы взаимодействия
