from typing import Iterable

from pydantic import UUID4
from sqlalchemy import Select, select

from app.domain.repositories.iphoto_repository import IListingPhotoRepository
from app.infrastructure.models.listing_photo_file_model import ListingPhotoFile
from app.presentation.schemas.photo_schema import ListingPhotoCreate, ListingPhotoDB


class ListingPhotoRepository(IListingPhotoRepository):
    def __init__(self, session) -> None:
        self._session = session

    async def create_photo(self, photo: ListingPhotoCreate) -> ListingPhotoDB:
        async with self._session() as session:
            db_photo = ListingPhotoFile(**photo.model_dump())
            session.add(db_photo)
            await session.commit()
            await session.refresh(db_photo)
            return ListingPhotoDB.model_validate(db_photo)

    async def list_photos(self, limit: int = 50, offset: int = 0) -> Iterable[ListingPhotoDB]:
        stmt: Select = (
            select(ListingPhotoFile)
            .order_by(ListingPhotoFile.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        async with self._session() as session:
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [ListingPhotoDB.model_validate(row) for row in rows]

    async def get_photo(self, photo_id: UUID4) -> ListingPhotoDB | None:
        stmt = select(ListingPhotoFile).where(ListingPhotoFile.id == photo_id)
        async with self._session() as session:
            result = await session.execute(stmt)
            photo = result.scalars().one_or_none()
            return ListingPhotoDB.model_validate(photo) if photo else None

    async def list_by_listing(self, listing_id: UUID4) -> Iterable[ListingPhotoDB]:
        stmt = (
            select(ListingPhotoFile)
            .where(ListingPhotoFile.listing_id == listing_id)
            .order_by(ListingPhotoFile.created_at.asc())
        )
        async with self._session() as session:
            result = await session.execute(stmt)
            photos = result.scalars().all()
            return [ListingPhotoDB.model_validate(photo) for photo in photos]
