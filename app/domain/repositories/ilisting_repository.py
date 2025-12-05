from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4
from sqlalchemy import Select

from app.domain.models.listing_update import ListingUpdate
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class IListingRepository(ABC):
    @abstractmethod
    async def save_listing(self, listings: Iterable[ListingIn]) -> Iterable[ListingDB]:
        """abstract method"""

    @abstractmethod
    async def get_listings(self, query: Select) -> ListingDB:
        """abstract method"""

    @abstractmethod
    async def delete_listing(self, lisitng_id: UUID4):
        """abstract method"""

    @abstractmethod
    async def get_single_listing(self, listing_id: UUID4) -> ListingDB | None:
        """abstract method"""

    @abstractmethod
    async def patch_listing(
        self, listing_id: UUID4, listing: ListingUpdate
    ) -> ListingDB:
        """abstract method"""
