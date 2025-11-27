import uuid
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.interfaces.inote_service import INoteService
from app.container import Container
from app.infrastructure.security import verify_token
from app.presentation.schemas.note_schema import NoteDb, NoteIn

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get("/notes/{listing_id}")
@inject
async def get_notes_by_listing_id(
    listing_id: uuid.UUID,
    service: INoteService = Depends(Provide[Container.note_service]),
) -> List[NoteDb]:
    return await service.get_notes_by_listing_id(listing_id)


@router.post("/notes")
@inject
async def create_note(
    note_in: NoteIn,
    service: INoteService = Depends(Provide[Container.note_service]),
) -> NoteDb:
    return await service.create_note(note_in)


@router.put("/notes/{note_id}")
@inject
async def update_note(
    note_id: uuid.UUID,
    note_in: NoteIn,
    service: INoteService = Depends(Provide[Container.note_service]),
) -> NoteDb:
    result = await service.update_note(note_id, note_in)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return result


@router.delete("/notes/{note_id}")
@inject
async def delete_note(
    note_id: uuid.UUID,
    service: INoteService = Depends(Provide[Container.note_service]),
) -> dict:
    success = await service.delete_note(note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return {"message": "Note deleted successfully"}
