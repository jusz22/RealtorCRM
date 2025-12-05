import uuid
from pathlib import Path
from typing import Iterable, Sequence

from pydantic import UUID4

from app.application.interfaces.iphoto_service import IListingPhotoService
from app.domain.dtos.photo_upload_dto import ListingPhotoUploadDTO
from app.domain.repositories.iphoto_repository import IListingPhotoRepository
from app.presentation.schemas.photo_schema import ListingPhotoCreate, ListingPhotoDB


class ListingPhotoServiceError(Exception):
    """Base exception for listing photo service failures."""


class PhotoTooLargeError(ListingPhotoServiceError):
    """Raised when an upload exceeds the configured size limit."""


class PhotoMissingError(ListingPhotoServiceError):
    """Raised when a stored photo cannot be located."""


class InvalidImageTypeError(ListingPhotoServiceError):
    """Raised when the uploaded file is not a supported image."""


class ListingPhotoService(IListingPhotoService):
    def __init__(
        self,
        repository: IListingPhotoRepository,
        storage_dir: str,
        max_upload_size_mb: int = 2,
    ) -> None:
        self._repository = repository
        self._storage_dir = Path(storage_dir)
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._max_upload_size_bytes = max_upload_size_mb * 1024 * 1024

    async def store_photo(self, photo: ListingPhotoUploadDTO) -> ListingPhotoDB:
        sanitized_name = self._sanitize_filename(photo.filename)
        size = len(photo.data)

        self._ensure_image_type(photo.content_type)

        if size == 0:
            raise ListingPhotoServiceError("Uploaded photo is empty.")

        if size > self._max_upload_size_bytes:
            raise PhotoTooLargeError(
                f"Photo {sanitized_name} exceeds {self._max_upload_size_bytes} bytes limit."
            )

        stored_name = self._build_stored_name(sanitized_name)
        target_path = self._storage_dir / stored_name
        try:
            target_path.write_bytes(photo.data)
        except OSError as exc:
            raise ListingPhotoServiceError(
                f"Failed to persist photo {sanitized_name}: {exc}"
            ) from exc

        metadata = ListingPhotoCreate(
            listing_id=photo.listing_id,
            original_name=sanitized_name,
            stored_name=stored_name,
            content_type=photo.content_type,
            size_bytes=size,
            storage_path=str(target_path),
        )
        return await self._repository.create_photo(metadata)

    async def store_photos(
        self, photos: Iterable[ListingPhotoUploadDTO]
    ) -> Sequence[ListingPhotoDB]:
        stored: list[ListingPhotoDB] = []
        for photo in photos:
            stored.append(await self.store_photo(photo))
        return stored

    async def get_photo(self, photo_id: UUID4) -> ListingPhotoDB | None:
        return await self._repository.get_photo(photo_id)

    async def read_photo(self, photo_id: UUID4) -> tuple[ListingPhotoDB, bytes]:
        metadata = await self._repository.get_photo(photo_id)
        if metadata is None:
            raise PhotoMissingError(f"Photo with id {photo_id} was not found.")

        data = self._read_photo_bytes(metadata)
        return metadata, data

    async def read_photos_by_listing(
        self, listing_id: UUID4
    ) -> Sequence[tuple[ListingPhotoDB, bytes]]:
        metadata_list = await self._repository.list_by_listing(listing_id)
        results: list[tuple[ListingPhotoDB, bytes]] = []
        for metadata in metadata_list:
            results.append((metadata, self._read_photo_bytes(metadata)))
        return results

    async def list_photos_by_listing(
        self, listing_id: UUID4
    ) -> Sequence[ListingPhotoDB]:
        return await self._repository.list_by_listing(listing_id)

    def _sanitize_filename(self, filename: str) -> str:
        sanitized = Path(filename).name.strip()
        if not sanitized:
            raise ListingPhotoServiceError("Filename cannot be empty.")
        return sanitized

    def _build_stored_name(self, sanitized_name: str) -> str:
        extension = Path(sanitized_name).suffix
        return f"{uuid.uuid4().hex}{extension}"

    def _ensure_image_type(self, content_type: str | None) -> None:
        if content_type is None or not content_type.startswith("image/"):
            raise InvalidImageTypeError("Only image uploads are supported.")

    def _read_photo_bytes(self, metadata: ListingPhotoDB) -> bytes:
        file_path = Path(metadata.storage_path)
        if not file_path.exists():
            raise PhotoMissingError(
                f"Stored photo for id {metadata.id} not found on disk at {file_path}."
            )

        try:
            return file_path.read_bytes()
        except OSError as exc:
            raise ListingPhotoServiceError(
                f"Unable to read photo {metadata.original_name}: {exc}"
            ) from exc
