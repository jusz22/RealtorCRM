from typing import List
from app.application.interfaces.ilisting_service import IListingService
from app.domain.repositories.ilisting_repository import IListingRepository
from app.infrastructure.models.listing_photo_model import ListingPhoto


class ListingService(IListingService):

    def __init__(self, repository: IListingRepository) -> None:
        self._repository = repository

    async def save_photos(self, photos: List[ListingPhoto]):
        return await self._repository.save_photos(photos=photos)