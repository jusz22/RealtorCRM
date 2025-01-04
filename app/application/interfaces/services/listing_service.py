from typing import List
from app.application.interfaces.ilisting_service import IListingService
from app.domain.repositories.ilisting_repository import IListingRepository
from app.infrastructure.models.listing_photo_model import ListingPhoto
from app.presentation.schemas.listing_schema import ListingDB, ListingIn


class ListingService(IListingService):

    def __init__(self, repository: IListingRepository) -> None:
        self._repository = repository

    async def save_photos(self, photos: List[ListingPhoto]):
        return await self._repository.save_photos(photos=photos)
    
    async def save_listing(self, listing: ListingIn) -> ListingDB:
        return await self._repository.save_listing(listing=listing)
    
    async def get_listing(self):
        return await self._repository.get_listing()