from typing import Iterable

from pydantic import UUID4
from sqlalchemy import select

from app.application.interfaces.ilisting_service import IListingService
from app.domain.dtos.filter_dto import FilterDTO
from app.domain.dtos.sort_options_dto import SortOptions
from app.domain.models.listing_update import ListingUpdate
from app.domain.repositories.ilisting_repository import IListingRepository
from app.infrastructure.models.listing_model import Listing
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class ListingService(IListingService):
    def __init__(self, repository: IListingRepository) -> None:
        self._repository = repository

    async def save_listing(self, listings: Iterable[ListingIn]) -> Iterable[ListingDB]:
        return await self._repository.save_listing(listings=listings)

    async def get_listings(
        self, sort_options: SortOptions, filter: FilterDTO
    ) -> Iterable[ListingDB]:
        query = select(Listing)
        sort_func = sort_options.get_sort_func()

        if filter is not None:
            filter_column = getattr(Listing, filter.field)
            filter_operator = filter.get_operator()
            filter_exp = getattr(filter_column, filter_operator)

            if filter_operator == "like":
                query = query.where(filter_exp(f"%{filter.value}%"))
            else:
                query = query.where(filter_exp(filter.value))

        if sort_func is not None:
            query = query.order_by(sort_func)

        return await self._repository.get_listings(query=query)

    async def remove_listing(self, listing_id: UUID4):
        return await self._repository.delete_listing(listing_id=listing_id)

    async def get_single_listing(self, listing_id: UUID4) -> ListingDB | None:
        return await self._repository.get_single_listing(listing_id=listing_id)

    async def patch_listing(
        self, listing_id: UUID4, listing: ListingUpdate
    ) -> ListingDB:
        return await self._repository.patch_listing(listing_id, listing)
