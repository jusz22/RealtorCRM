import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class NoteIn(BaseModel):
    note: str
    listing_id: UUID4
    user_id: int


class NoteDb(NoteIn):
    id: UUID4
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
