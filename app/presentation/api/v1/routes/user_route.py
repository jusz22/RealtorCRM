
import stat
from typing import Iterable
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from dependency_injector.wiring import inject, Provide

from app.application.interfaces.iuser_service import IUserService
from app.container import Container
from app.infrastructure.security import get_password_hash
from app.presentation.schemas.user_schema import UserIn, UserDB



router = APIRouter()

@router.get("/users", response_model=Iterable[UserDB], status_code=200)
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service])) -> Iterable:
    users = await service.get_all()

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