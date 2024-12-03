from typing import List
from app.domain.repositories.ilisting_repository import IListingRepository
from  sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.listing_photo_model import ListingPhoto

class ListingRepository(IListingRepository):
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_photos(self, photos: List[ListingPhoto]) -> None:
        async with self._session as session:
            session.add_all(photos)
            await session.commit()
