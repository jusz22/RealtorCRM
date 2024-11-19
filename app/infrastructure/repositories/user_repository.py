from typing import Iterable

from sqlalchemy import select

from app.infrastructure.models.user_model import User
from app.domain.repositories.iuser_repository import IUserRepository
from app.presentation.schemas.user_schema import UserCreate, UserInDB

from  sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> Iterable[UserInDB]:
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()

        return [UserInDB.model_validate(user) for user in users]
        
    async def save_user(self, user: UserCreate) -> UserInDB:
        
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        
        async with self.session as session:
            session.add(db_user)
            await session.commit()
        return UserInDB.model_validate(db_user)
    
    async def get_user_by_username(self, username: str) -> User | None:
        async with self.session as session:
            result = await session.execute(select(User).where(User.username==username))
            user = result.scalar_one_or_none()
            return user