from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.models.listing_photo_model import ListingPhoto
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class IListingRepository(ABC):
    @abstractmethod
    async def save_photos(self, photos: List[ListingPhoto]) -> None:
        """abstract method"""
    
    @abstractmethod
    async def save_listing(self, listing: ListingIn) -> ListingIn:
        """abstract method"""

    async def get_listing(self) -> ListingDB:
        """abstract method"""