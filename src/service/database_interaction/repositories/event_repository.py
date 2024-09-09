from typing import List, Optional

from sqlalchemy.orm import Session

from src.service.database_interaction.dto.event import EventCreateDTO, EventDTO
from src.service.database_interaction.orm_models.events import Events
from src.service.database_interaction.orm_models.users import Users


class EventRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, event_create_dto: EventCreateDTO, admin_id: int) -> None:
        admin = self._session.query(Users).filter(Users.id == admin_id).first()
        if not admin:
            raise ValueError("Admin user not found")

        event = Events(
            title=event_create_dto.title,
            description=event_create_dto.description,
            admin=admin,  # Set the admin relationship
        )
        self._session.add(event)
        self._session.commit()
        self._session.refresh(event)

    def read_by_title(self, title: str) -> Optional[EventDTO]:
        event = self._session.query(Events).filter(Events.title == title).first()
        return EventDTO.model_validate(event) if event else None

    def delete(self, event_id: int):
        event = self._session.query(Events).filter(Events.id == event_id).first()
        if not event:
            return

        self._session.delete(event)
        self._session.commit()

    def add_users_to_event(self, event_id: int, user_ids: List[int]) -> None:
        event = self._session.query(Events).filter(Events.id == event_id).first()
        if not event:
            return

        users = self._session.query(Users).filter(Users.id.in_(user_ids)).all()
        for user in users:
            event.users.append(user)

        self._session.commit()

    def is_admin(self, event_title: str, user_telegram_id: str) -> bool:
        event = self.read_by_title(event_title)
        if not event:
            return False

        admin_user = self._session.query(Users).filter(Users.telegram_id == user_telegram_id).first()
        if not admin_user:
            return False

        return event.admin_id == admin_user.id
