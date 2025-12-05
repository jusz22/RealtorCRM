import datetime
from pydantic import BaseModel, ConfigDict, UUID4


class ListingPhotoCreate(BaseModel):
    listing_id: UUID4
    original_name: str
    stored_name: str
    content_type: str | None
    size_bytes: int
    storage_path: str


class ListingPhotoDB(ListingPhotoCreate):
    id: UUID4
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


class ListingPhotoPayload(BaseModel):
    id: UUID4
    listing_id: UUID4
    original_name: str
    content_type: str | None
    size_bytes: int
    data: str
