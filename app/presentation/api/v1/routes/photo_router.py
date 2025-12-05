import base64
from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import UUID4

from app.application.interfaces.iphoto_service import IListingPhotoService
from app.application.interfaces.services.photo_service import (
    InvalidImageTypeError,
    ListingPhotoServiceError,
    PhotoTooLargeError,
)
from app.container import Container
from app.domain.dtos.photo_upload_dto import ListingPhotoUploadDTO
from app.infrastructure.config import config
from app.infrastructure.security import verify_token
from app.presentation.schemas.photo_schema import ListingPhotoDB, ListingPhotoPayload

router = APIRouter(dependencies=[Depends(verify_token)])

MAX_UPLOAD_SIZE_BYTES = config.MAX_UPLOAD_SIZE_MB * 1024 * 1024


def _ensure_image(upload_file: UploadFile) -> None:
    if upload_file.content_type is None or not upload_file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(status_code=415, detail="Only image uploads are allowed.")


async def _upload_to_dto(
    upload_file: UploadFile, listing_id: UUID4
) -> ListingPhotoUploadDTO:
    data = await upload_file.read(MAX_UPLOAD_SIZE_BYTES + 1)
    if len(data) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Photo exceeds {config.MAX_UPLOAD_SIZE_MB}MB limit.",
        )
    _ensure_image(upload_file)
    return ListingPhotoUploadDTO(
        listing_id=listing_id,
        filename=upload_file.filename or "uploaded_photo",
        content_type=upload_file.content_type,
        data=data,
    )


@router.post(
    "/listings/{listing_id}/photos", response_model=ListingPhotoDB, status_code=201
)
@inject
async def upload_photo(
    listing_id: UUID4,
    file: Annotated[UploadFile, File(...)],
    service: IListingPhotoService = Depends(Provide[Container.photo_service]),
) -> ListingPhotoDB:
    try:
        dto = await _upload_to_dto(file, listing_id)
        stored = await service.store_photo(dto)
    except PhotoTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except InvalidImageTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except ListingPhotoServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await file.close()
    return stored


@router.post(
    "/listings/{listing_id}/photos/batch",
    response_model=list[ListingPhotoDB],
    status_code=201,
)
@inject
async def upload_photos(
    listing_id: UUID4,
    files: Annotated[list[UploadFile], File(...)],
    service: IListingPhotoService = Depends(Provide[Container.photo_service]),
) -> list[ListingPhotoDB]:
    try:
        dtos = [await _upload_to_dto(file, listing_id) for file in files]
        stored = await service.store_photos(dtos)
    except PhotoTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except InvalidImageTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except ListingPhotoServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        for file in files:
            await file.close()
    return list(stored)


@router.get("/listings/{listing_id}/photos", response_model=list[ListingPhotoDB])
@inject
async def get_photo_metadata(
    listing_id: UUID4,
    service: IListingPhotoService = Depends(Provide[Container.photo_service]),
) -> list[ListingPhotoDB]:
    metadata = await service.list_photos_by_listing(listing_id)
    return list(metadata)


@router.get(
    "/listings/{listing_id}/photos/download",
    response_model=list[ListingPhotoPayload],
)
@inject
async def download_listing_photos(
    listing_id: UUID4,
    service: IListingPhotoService = Depends(Provide[Container.photo_service]),
):
    try:
        photos = await service.read_photos_by_listing(listing_id)
    except ListingPhotoServiceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    payload: list[ListingPhotoPayload] = []
    for metadata, data in photos:
        payload.append(
            ListingPhotoPayload(
                id=metadata.id,
                listing_id=metadata.listing_id,
                original_name=metadata.original_name,
                content_type=metadata.content_type,
                size_bytes=metadata.size_bytes,
                data=base64.b64encode(data).decode("utf-8"),
            )
        )
    return payload


@router.get("/photos/{photo_id}/file")
@inject
async def download_photo_file(
    photo_id: UUID4,
    service: IListingPhotoService = Depends(Provide[Container.photo_service]),
):
    metadata = await service.get_photo(photo_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    file_path = Path(metadata.storage_path)
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Stored photo missing")

    return FileResponse(
        path=file_path,
        media_type=metadata.content_type,
        filename=metadata.original_name,
    )
