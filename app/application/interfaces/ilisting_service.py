from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from app.domain.dtos.filter_dto import FilterDTO
from app.domain.dtos.sort_options_dto import SortOptions
from app.domain.models.listing_update import ListingUpdate
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class IListingService(ABC):
    @abstractmethod
    async def save_listing(self, listings: Iterable[ListingIn]) -> Iterable[ListingDB]:
        """abstract method"""

    @abstractmethod
    async def get_listings(
        self, sort_options: SortOptions, filter: FilterDTO
    ) -> Iterable[ListingDB]:
        """

        Returns:
                ListingDB: _description_
        """

    @abstractmethod
    async def remove_listing(self, listing_id: UUID4):
        """abstract method"""

    @abstractmethod
    async def get_single_listing(self, listing_id: UUID4) -> ListingDB | None:
        """abstract method"""

    @abstractmethod
    async def patch_listing(
        self, listing_id: UUID4, listing: ListingUpdate
    ) -> ListingDB:
        """abstract method"""
