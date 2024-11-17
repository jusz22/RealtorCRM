
from typing import Iterable
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.application.interfaces.iuser_service import IUserService
from app.container import Container
from app.presentation.schemas.user_schema import UserInDB


router = APIRouter()

@router.get("/user", response_model=Iterable[UserInDB], status_code=200)
@inject
async def get_all_users(service: IUserService = Depends(Provide[Container.user_service])) -> Iterable:
    users = await service.get_all()

    return users