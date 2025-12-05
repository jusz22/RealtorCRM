from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from app.presentation.schemas.photo_schema import ListingPhotoCreate, ListingPhotoDB


class IListingPhotoRepository(ABC):
    @abstractmethod
    async def create_photo(self, photo: ListingPhotoCreate) -> ListingPhotoDB:
        """Persist metadata for a stored listing photo."""

    @abstractmethod
    async def list_photos(
        self, limit: int = 50, offset: int = 0
    ) -> Iterable[ListingPhotoDB]:
        """Return stored photos with optional pagination."""

    @abstractmethod
    async def get_photo(self, photo_id: UUID4) -> ListingPhotoDB | None:
        """Fetch stored photo metadata by identifier."""

    @abstractmethod
    async def list_by_listing(self, listing_id: UUID4) -> Iterable[ListingPhotoDB]:
        """Return all photos associated with a given listing."""
