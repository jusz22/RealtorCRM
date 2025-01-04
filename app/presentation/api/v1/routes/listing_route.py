from typing import List
from fastapi import APIRouter, Depends, UploadFile
from dependency_injector.wiring import inject, Provide
from app.application.interfaces.ilisting_service import IListingService
from app.container import Container
from app.infrastructure.models.listing_photo_model import ListingPhoto
from app.presentation.schemas.listing_schema import ListingDB, ListingIn

router = APIRouter()

@router.post("/listings/{listing_id}/photos", status_code=200)
@inject
async def add_listing_photos(
    listing_id: int,
    files: List[UploadFile],
    service: IListingService = Depends(Provide[Container.listing_service])
):
    uploaded_photos = []

    for file in files:
        image_data = await file.read()
        photo = ListingPhoto(listing_id=listing_id, image_data=image_data)
        uploaded_photos.append(photo)
        await file.close()

    await service.save_photos(uploaded_photos)
    
    return {"Done": "done"}

@router.post("/listings")
@inject
async def add_lisitng(
    listing: ListingIn,
    service: IListingService = Depends(Provide[Container.listing_service])
) -> ListingDB:
    
    return await service.save_listing(listing=listing)

@router.get("/listings")
@inject
async def get_listing(
    service: IListingService = Depends(Provide[Container.listing_service])) -> ListingDB:

    return await service.get_listing()