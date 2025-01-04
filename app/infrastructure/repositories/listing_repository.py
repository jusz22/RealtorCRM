from typing import List

from sqlalchemy import select
from app.domain.repositories.ilisting_repository import IListingRepository
from  sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.listing_model import Listing
from app.infrastructure.models.listing_photo_model import ListingPhoto
from app.presentation.schemas.listing_schema import ListingDB, ListingIn

class ListingRepository(IListingRepository):
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_photos(self, photos: List[ListingPhoto]) -> None:
        async with self._session as session:
            session.add_all(photos)
            await session.commit()

    async def save_listing(self, listing: ListingIn) -> ListingDB:
        
        db_lisitng = Listing(**listing.model_dump())
        
        async with self._session as session:
            session.add(db_lisitng)
            await session.commit()
            await session.refresh(db_lisitng)
            return ListingDB(
                id=db_lisitng.id,
                **listing.model_dump())
        
    async def get_listing(self):
        async with self._session as session:
            result = await session.execute(select(Listing))
            listings = result.scalars().all()
        return listings
