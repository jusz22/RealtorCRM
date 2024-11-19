from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.infrastructure.config import config
import jwt

from app.presentation.schemas.token_schema import TokenData


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_password_hash(password: str) -> str:
    return password_context.hash(password)

async def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

async def create_token(data: dict, expieres_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expieres_delta:
        expire = datetime.now(timezone.utc) + expieres_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALGORITHM)
    return encoded_jwt

async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        payload = jwt.decode(token, key=config.SECRET_KEY, algorithms=config.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await self._repository.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    
    return user