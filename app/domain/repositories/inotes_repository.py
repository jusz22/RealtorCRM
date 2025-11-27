from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from app.presentation.schemas.note_schema import NoteDb, NoteIn


class INotesRepository(ABC):
    @abstractmethod
    async def saveNote(self, note: NoteIn) -> NoteDb:
        """
        docstring
        """

    @abstractmethod
    async def get_notes(self, listing_id: UUID) -> Iterable[NoteDb]:
        """
        docstring
        """

    @abstractmethod
    async def delete_note(self, note_id: UUID) -> NoteDb:
        """
        docstring
        """
