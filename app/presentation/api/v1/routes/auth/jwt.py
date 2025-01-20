from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from dependency_injector.wiring import Provide, inject

from app.application.interfaces.iuser_service import IUserService
from app.infrastructure.config import config
from app.infrastructure.security import create_token, get_password_hash
from app.presentation.schemas.token_schema import Token
from app.infrastructure.security import authenticate_user
from app.presentation.schemas.user_schema import UserDB, UserIn
from app.container import Container


router = APIRouter()

@router.post("/login", response_model=Token)
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:

    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_token({"sub": user.username}, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=UserDB)
@inject
async def register(user_data: UserIn, service: IUserService = Depends(Provide[Container.user_service])):
        try:
            user_data.hashed_password = await get_password_hash(user_data.hashed_password)
        
            added_user = await service.save_user(user_data)
    
            return added_user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or password already exists")