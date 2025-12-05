from typing import Iterable

from pydantic import UUID4
from sqlalchemy import Select, delete, select, update

from app.domain.models.listing_update import ListingUpdate
from app.domain.repositories.ilisting_repository import IListingRepository
from app.infrastructure.models.listing_model import Listing
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class ListingRepository(IListingRepository):
    def __init__(self, session) -> None:
        self._session = session

    async def save_listing(self, listings: Iterable[ListingIn]) -> Iterable[ListingDB]:
        listings_data = list(listings)

        if not listings_data:
            return []

        db_listing = [Listing(**listing.model_dump()) for listing in listings_data]

        async with self._session() as session:
            session.add_all(db_listing)
            await session.flush()

            for listing in db_listing:
                await session.refresh(listing)

            saved_listings = [
                ListingDB.model_validate(listing) for listing in db_listing
            ]

            await session.commit()
            return saved_listings

    async def get_listings(self, query: Select) -> Iterable[ListingDB]:
        async with self._session() as session:
            result = await session.execute(query)
            listings = result.scalars().all()
            return [ListingDB.model_validate(listing) for listing in listings]

    async def get_single_listing(self, listing_id) -> ListingDB | None:
        async with self._session() as session:
            result = await session.execute(
                select(Listing).where(Listing.id == listing_id)
            )
            listing = result.scalars().one_or_none()
            return ListingDB.model_validate(listing) if listing is not None else None

    async def delete_listing(self, listing_id: UUID4) -> ListingDB | None:
        async with self._session() as session:
            result = await session.execute(
                select(Listing).where(Listing.id == listing_id)
            )
            listing = result.scalars().one_or_none()

            if listing is None:
                return None

            await session.execute(delete(Listing).where(Listing.id == listing_id))
            await session.commit()
            return ListingDB.model_validate(listing)

    async def patch_listing(
        self, listing_id: UUID4, listing_update: ListingUpdate
    ) -> ListingDB | None:
        async with self._session() as session:
            # Prepare only the fields that are set
            update_data = listing_update.model_dump(exclude_unset=True)
            if not update_data:
                return None
            # Perform the update
            await session.execute(
                update(Listing).where(Listing.id == listing_id).values(**update_data)
            )
            await session.commit()
            return await self.get_single_listing(listing_id)
