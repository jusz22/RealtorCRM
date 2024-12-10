from typing import Iterable

from sqlalchemy import delete, select

from app.infrastructure.models.user_model import User
from app.domain.repositories.iuser_repository import IUserRepository
from app.presentation.schemas.user_schema import UserIn, UserDB

from  sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_users(self, query) -> Iterable[UserDB]:
        async with self._session as session:
            result = await session.execute(query)
            users = result.scalars().all()

        return [UserDB.model_validate(user) for user in users]
        
    async def save_user(self, user: UserIn) -> UserDB:
        
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        
        async with self._session as session:
            session.add(db_user)
            await session.commit()
        return UserDB.model_validate(db_user)
    
    async def get_user(self, user_id) -> UserDB | None:
        async with self._session as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            return UserDB.model_validate(user) if user is not None else None
        
    async def delete_user(self, user_id) -> UserDB | None:
        async with self._session as session:
            user = await self.get_user(user_id=user_id)
            if not user: 
                return None
            await session.execute(delete(User).where(User.id == user_id))
            await session.commit()
            return UserDB.model_validate(user)