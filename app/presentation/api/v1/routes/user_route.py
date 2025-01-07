from typing import Annotated, Iterable
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from dependency_injector.wiring import inject, Provide

from app.application.interfaces.iuser_service import IUserService
from app.container import Container
from app.domain.dtos.sort_options_dto import SortOptions
from app.infrastructure.models.user_model import User
from app.infrastructure.security import get_password_hash
from app.presentation.schemas.user_schema import UserIn, UserDB



router = APIRouter()

@router.get("/users", response_model=Iterable[UserDB], status_code=200)
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service]),
    sort_order: Annotated[str | None, Query(description='Sort order')] = None,
    sort_by: Annotated[str | None, Query(description='Column to sort by')] = None) -> Iterable:

    if (sort_by not in User.__annotations__ or sort_by == 'hashed_password') and (sort_by is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Column '{sort_by}' doesn't exist"
        )
        
    sort_options = SortOptions(
        column=sort_by,
        order=sort_order)

    users = await service.get_all(sort_options=sort_options)

    return users

@router.post("/users", response_model=UserDB, status_code=200)
@inject
async def add_user(user_data: UserIn, service: IUserService = Depends(Provide[Container.user_service])) -> UserDB:

    try:
        user_data.hashed_password = await get_password_hash(user_data.hashed_password)
        
        added_user = await service.save_user(user_data)
    
        return added_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or password already exists")
    
@router.get("/users/{id}", response_model=UserDB, status_code=200)
@inject
async def get_user(
    id: int,
    service: IUserService = Depends(Provide[Container.user_service])) -> UserDB:

    user = await service.get_user(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is no user of id: {id}"
        )

    return user

@router.delete("/users/{id}", response_model=UserDB, status_code=200)
@inject
async def delete_user(
    id: int,
    service: IUserService = Depends(Provide[Container.user_service])) -> UserDB:

    user = await service.delete_user(user_id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are trying to delete a user that doesn't exist"
        )
    return user