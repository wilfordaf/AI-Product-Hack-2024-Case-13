from typing import List, Optional

from sqlalchemy.orm import Session

from src.service.database_interaction.dto.event import EventCreateDTO, EventDTO
from src.service.database_interaction.orm_models.events import Events
from src.service.database_interaction.orm_models.users import Users


class EventRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, event_create_dto: EventCreateDTO) -> None:
        event = Events(title=event_create_dto.title, description=event_create_dto.description)
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
