from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from app.application.interfaces.iuser_service import IUserService
from app.presentation.schemas.token_schema import Token
from app.container import Container


router = APIRouter()

@router.post("/login")
@inject
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: IUserService = Depends(Provide[Container.user_service])):

    user = await service.authenticate_user(form_data.username, form_data.password)
    return user



