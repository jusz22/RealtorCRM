from dataclasses import dataclass

from pydantic import UUID4


@dataclass(slots=True)
class ListingPhotoUploadDTO:
    listing_id: UUID4
    filename: str
    content_type: str | None
    data: bytes
