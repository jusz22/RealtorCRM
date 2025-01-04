from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.models.listing_photo_model import ListingPhoto
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class IListingService(ABC):
    @abstractmethod
    async def save_photos(self, photos: List[ListingPhoto]):
        """abstract method"""

    @abstractmethod
    async def save_listing(self, listing: ListingIn) -> ListingIn:
        """abstract method"""

    @abstractmethod
    async def get_listing(self) -> ListingDB:
        """

        Returns:
            ListingDB: _description_
        """