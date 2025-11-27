import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from app.presentation.schemas.note_schema import NoteDb, NoteIn


class INoteService(ABC):
    @abstractmethod
    async def get_notes_by_listing_id(self, listing_id: uuid.UUID) -> List[NoteDb]:
        """abstract method"""

    @abstractmethod
    async def create_note(self, note_in: NoteIn) -> NoteDb:
        """abstract method"""

    @abstractmethod
    async def update_note(
        self, note_id: uuid.UUID, note_in: NoteIn
    ) -> Optional[NoteDb]:
        """abstract method"""

    @abstractmethod
    async def delete_note(self, note_id: uuid.UUID) -> bool:
        """abstract method"""
