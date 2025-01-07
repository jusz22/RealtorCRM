from typing import Iterable, List

from pydantic import UUID4
from sqlalchemy import Select, delete, select
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
        
    async def get_listings(self, query: Select) -> Iterable[ListingDB]:
        async with self._session as session:
            result = await session.execute(query)
            listings = result.scalars().all()
        return [ListingDB.model_validate(listing) for listing in listings]
    
    async def get_single_listing(self, listing_id) -> ListingDB | None:
        async with self._session as session:
            result = await session.execute(select(Listing).where(Listing.id == listing_id))
            listing = result.scalars().one_or_none()
        return ListingDB.model_validate(listing) if listing is not None else None
    
    async def delete_listing(self, listing_id: UUID4) -> ListingDB | None:
        
        async with self._session as session:
            listing = await self.get_single_listing(lisitng_id=listing_id)

            if not listing:
                return None
            
            await session.execute(delete(Listing).where(Listing.id==listing_id))
            await session.commit()
            return listing