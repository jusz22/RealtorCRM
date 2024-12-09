from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject

from app.infrastructure.config import config
from app.infrastructure.models.user_model import User
from app.infrastructure.security import create_token, get_current_user
from app.presentation.schemas.token_schema import Token
from app.infrastructure.security import authenticate_user


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

@router.post('/test-token', summary="Test if the access token is valid")
async def test_token(user: User = Depends(get_current_user)):
    return user


