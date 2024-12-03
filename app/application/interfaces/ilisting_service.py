from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.models.listing_photo_model import ListingPhoto


class IListingService(ABC):
    @abstractmethod
    async def save_photos(self, photos: List[ListingPhoto]):
        """abstract method"""