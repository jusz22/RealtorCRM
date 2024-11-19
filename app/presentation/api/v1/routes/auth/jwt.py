from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from app.infrastructure.config import config
from app.application.interfaces.iuser_service import IUserService
from app.infrastructure.security import create_token
from app.presentation.schemas.token_schema import Token
from app.container import Container


router = APIRouter()

@router.post("/login")
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    service: IUserService = Depends(Provide[Container.user_service])) -> Token:

    user = await service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token_expires = timedelta(config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_token({"sub": user.username}, access_token_expires)

    return Token(token=access_token, token_type="bearer")




