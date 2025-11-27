from typing import List, Optional
import uuid
from app.infrastructure.repositories.note_repository import NoteRepository
from app.presentation.schemas.note_schema import NoteDb, NoteIn
from app.application.interfaces.inote_service import INoteService

class NoteService(INoteService):
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def get_notes_by_listing_id(self, listing_id: uuid.UUID) -> List[NoteDb]:
        return await self.note_repository.get_by_id(listing_id)

    async def create_note(self, note_in: NoteIn) -> NoteDb:
        return await self.note_repository.create(note_in)

    async def update_note(self, note_id: uuid.UUID, note_in: NoteIn) -> Optional[NoteDb]:
        return await self.note_repository.update(note_id, note_in)

    async def delete_note(self, note_id: uuid.UUID) -> bool:
        return await self.note_repository.delete(note_id)
