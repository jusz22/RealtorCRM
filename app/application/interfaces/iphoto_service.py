from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from pydantic import UUID4

from app.domain.dtos.photo_upload_dto import ListingPhotoUploadDTO
from app.presentation.schemas.photo_schema import ListingPhotoDB


class IListingPhotoService(ABC):
    @abstractmethod
    async def store_photo(self, photo: ListingPhotoUploadDTO) -> ListingPhotoDB:
        """Persist a single listing photo to disk and metadata to the repository."""

    @abstractmethod
    async def store_photos(
        self, photos: Iterable[ListingPhotoUploadDTO]
    ) -> Sequence[ListingPhotoDB]:
        """Persist multiple listing photos."""

    @abstractmethod
    async def get_photo(self, photo_id: UUID4) -> ListingPhotoDB | None:
        """Fetch stored metadata for a photo."""

    @abstractmethod
    async def list_photos_by_listing(
        self, listing_id: UUID4
    ) -> Sequence[ListingPhotoDB]:
        """Return all stored photo metadata for a listing."""

    @abstractmethod
    async def read_photo(self, photo_id: UUID4) -> tuple[ListingPhotoDB, bytes]:
        """Return photo metadata along with its binary content."""

    @abstractmethod
    async def read_photos_by_listing(
        self, listing_id: UUID4
    ) -> Sequence[tuple[ListingPhotoDB, bytes]]:
        """Return all photo binaries for a listing."""
