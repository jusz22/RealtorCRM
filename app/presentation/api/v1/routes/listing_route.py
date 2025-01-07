import code
from http.client import NOT_FOUND
from sqlalchemy.exc import IntegrityError
from typing import Annotated, Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from dependency_injector.wiring import inject, Provide
from pydantic import UUID4
from app.application.interfaces.ilisting_service import IListingService
from app.container import Container
from app.domain.dtos.sort_options_dto import SortOptions
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
async def add_listing(
    listing: ListingIn,
    service: IListingService = Depends(Provide[Container.listing_service])
) -> ListingDB | Dict:
    
    try:
        added_lisitng = await service.save_listing(listing=listing)
        return added_lisitng
    except IntegrityError:
        return {"title": "already exists"}


@router.get("/listings")
@inject
async def get_listings(
    service: IListingService = Depends(Provide[Container.listing_service]),
    sort_order: Annotated[str | None, Query(description='Sort order')] = None,
    sort_by: Annotated[str | None, Query(description='Column to sort by')] = None) -> ListingDB | Any:

    sort_options = SortOptions(
        column=sort_by,
        order=sort_order)
    
    return await service.get_listings(sort_options=sort_options)

@router.delete("/listings/{listing_id}")
@inject
async def delete_listing(
    listing_id: UUID4,
    service: IListingService = Depends(Provide[Container.listing_service])):

    deleted_lisiting = await service.remove_listing(listing_id=listing_id)

    return deleted_lisiting

@router.get("/listings/{listing_id}")
@inject
async def get_single_listing(
    listing_id: UUID4,
    service: IListingService = Depends(Provide[Container.listing_service])):
    
    listing = await service.get_single_listing(listing_id=listing_id)

    if listing is None:
        raise HTTPException(status_code=404, detail=f"No listing of id {listing_id} was found")
    return listing