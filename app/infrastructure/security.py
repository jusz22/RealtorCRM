from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.config import config
import jwt
from dependency_injector.wiring import Provide, inject
from app.container import Container

from app.infrastructure.models.user_model import User
from app.presentation.schemas.token_schema import TokenData, TokenPayload


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")

async def get_password_hash(password: str) -> str:
    return password_context.hash(password)

async def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

async def authenticate_user(username: str, password: str) -> User | None:
    user = await get_user_by_username(username=username)
    if not user:
        return None
    if not await verify_password(password = password, hashed_password = user.hashed_password):
        return None
    return user

@inject
async def get_user_by_username(username: str, session: AsyncSession = Depends(Provide[Container.db])) -> User | None:
        print(username)
        result = await session.execute(select(User).where(User.username==username))
        return result.scalar_one_or_none()

async def create_token(data: dict, expieres_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expieres_delta:
        expire = datetime.now(timezone.utc) + expieres_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALGORITHM)
    return encoded_jwt

async def get_current_user(
        token: str = Depends(oauth2_scheme)) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        payload = jwt.decode(token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM])
        token_data = TokenPayload(**payload)
        username: str = token_data.sub
        if username is None:          
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username(username=username)

    if user is None:
        raise credentials_exception
    
    return user