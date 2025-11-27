import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.notes_model import Notes
from app.presentation.schemas.note_schema import NoteDb, NoteIn


class NoteRepository:
    def __init__(self, session):
        self._session = session

    async def get_by_id(self, listing_id: uuid.UUID) -> list[NoteDb]:
        stmt = select(Notes).where(Notes.listing_id == listing_id)
        async with self._session() as session:
            result = await session.execute(stmt)
            notes = result.scalars().all()
            return [NoteDb.model_validate(n) for n in notes]

    async def create(self, note_in: NoteIn) -> NoteDb:
        note = Notes(
            note=note_in.note, listing_id=note_in.listing_id, user_id=note_in.user_id
        )
        async with self._session() as session:
            session.add(note)
            await session.commit()
            await session.refresh(note)
            return NoteDb.model_validate(note)

    async def update(self, note_id: uuid.UUID, note_in: NoteIn) -> NoteDb | None:
        stmt = select(Notes).where(Notes.id == note_id)
        async with self._session() as session:
            result = await session.execute(stmt)
            note = result.scalars().first()
            if not note:
                return None
            note.note = note_in.note
            note.listing_id = note_in.listing_id
            note.user_id = note_in.user_id
            await session.commit()
            await session.refresh(note)
            return NoteDb.model_validate(note)

    async def delete(self, note_id: uuid.UUID) -> bool:
        stmt = select(Notes).where(Notes.id == note_id)
        async with self._session() as session:
            result = await session.execute(stmt)
            note = result.scalars().first()
            if not note:
                return False
            await session.delete(note)
            await session.commit()
            return True
