from typing import List, Optional

from sqlalchemy.orm import Session, sessionmaker

from src.service.database_interaction.dto.event import (
    EventCreateDTO,
    EventDTO,
    EventUpdateUserDTO,
)
from src.service.database_interaction.dto.user import UserDTO
from src.service.database_interaction.orm_models.events import Events
from src.service.database_interaction.orm_models.users import Users


class EventRepository:
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session_maker = session_maker

    def create(self, event_create_dto: EventCreateDTO) -> None:
        with self._session_maker() as session:
            admin = session.query(Users).filter(Users.telegram_id == event_create_dto.admin_telegram_id).first()
            if not admin:
                return

            event = Events(
                title=event_create_dto.title,
                description=event_create_dto.description,
                admin=admin,
            )
            session.add(event)
            session.commit()
            session.refresh(event)

    def read_by_title(self, title: str) -> Optional[EventDTO]:
        with self._session_maker() as session:
            event = session.query(Events).filter(Events.title == title).first()
            return EventDTO.model_validate(event) if event else None

    def delete(self, event_id: int):
        with self._session_maker() as session:
            event = session.query(Events).filter(Events.id == event_id).first()
            if not event:
                return

            session.delete(event)
            session.commit()

    def add_users_to_event(self, event_id: int, user_ids: List[int]) -> None:
        with self._session_maker() as session:
            event = session.query(Events).filter(Events.id == event_id).first()
            if not event:
                return

            users = session.query(Users).filter(Users.id.in_(user_ids)).all()
            for user in users:
                event.users.append(user)

            session.commit()

    def is_admin(self, event_title: str, user_telegram_id: str) -> bool:
        with self._session_maker() as session:
            event = self.read_by_title(event_title)
            if not event:
                return False

            admin_user = session.query(Users).filter(Users.telegram_id == user_telegram_id).first()
            if not admin_user:
                return False

            return bool(event.admin_id == admin_user.id)

    def get_users_by_event_title(self, event_title: str) -> List[UserDTO]:
        with self._session_maker() as session:
            event = session.query(Events).filter(Events.title == event_title).first()
            if not event:
                return []

            users = event.users
            return [UserDTO.model_validate(user) for user in users]

    def add_user_to_event(self, event_update_user_dto: EventUpdateUserDTO) -> None:
        with self._session_maker() as session:
            event = session.query(Events).filter(Events.title == event_update_user_dto.title).first()
            if not event:
                return

            user = session.query(Users).filter(Users.telegram_id == event_update_user_dto.user_telegram_id).first()
            if not user:
                return

            if user not in event.users:
                event.users.append(user)
                session.commit()
