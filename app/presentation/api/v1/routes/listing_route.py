from typing import Annotated, Iterable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError

from app.application.interfaces.ilisting_service import IListingService
from app.container import Container
from app.domain.dtos.filter_dto import FilterDTO
from app.domain.dtos.sort_options_dto import SortOptions
from app.domain.models.listing_update import ListingUpdate
from app.infrastructure.const import OPERATORS
from app.infrastructure.security import verify_token
from app.presentation.schemas.listing_schema import ListingDB, ListingIn

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post("/listings", response_model=list[ListingDB], status_code=201)
@inject
async def add_listing(
    listings: Annotated[Iterable[ListingIn], Body()],
    service: IListingService = Depends(Provide[Container.listing_service]),
) -> list[ListingDB]:
    try:
        saved_listings = await service.save_listing(listings=listings)
        return saved_listings
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="A listing with this title already exists."
        )


@router.get("/listings")
@inject
async def get_listings(
    service: IListingService = Depends(Provide[Container.listing_service]),
    sort_order: Annotated[str | None, Query(description="Sort order")] = None,
    sort_by: Annotated[str | None, Query(description="Column to sort by")] = None,
    filter: Annotated[
        str | None,
        Query(
            description="Filter format 'field_operator=value. Avilable operators [gt, gte, lt, lte, eq, ne, like]'"
        ),
    ] = None,
) -> Iterable[ListingDB]:
    try:
        sort_options = SortOptions(column=sort_by, order=sort_order)

        if filter is not None:
            field_operator, value = filter.split("=")
            field, operator = field_operator.split("_")

            if operator not in OPERATORS:
                raise ValueError(f"Incorrect operator {operator}")

            value = int(value) if value.isdigit() else value

            filter = FilterDTO(field=field, operator=operator, value=value)

        return await service.get_listings(sort_options=sort_options, filter=filter)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Wrong filter format {filter}. Error {e}"
        )


@router.delete("/listings/{listing_id}")
@inject
async def delete_listing(
    listing_id: UUID4,
    service: IListingService = Depends(Provide[Container.listing_service]),
):
    deleted_lisiting = await service.remove_listing(listing_id=listing_id)

    return deleted_lisiting


@router.get("/listings/{listing_id}")
@inject
async def get_single_listing(
    listing_id: UUID4,
    service: IListingService = Depends(Provide[Container.listing_service]),
):
    listing = await service.get_single_listing(listing_id=listing_id)

    if listing is None:
        raise HTTPException(
            status_code=404, detail=f"No listing of id {listing_id} was found"
        )
    return listing


@router.patch("/listings/{listing_id}", response_model=ListingDB)
@inject
async def patch_listing(
    listing_id: UUID4 = Path(..., description="Listing ID"),
    listing: ListingUpdate = Body(...),
    service: IListingService = Depends(Provide[Container.listing_service]),
):
    updated = await service.patch_listing(listing_id, listing)
    if not updated:
        raise HTTPException(
            status_code=404, detail=f"No listing of id {listing_id} was found"
        )
    return updated
