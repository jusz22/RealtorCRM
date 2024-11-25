from typing import Iterable

from sqlalchemy import select

from app.infrastructure.models.user_model import User
from app.domain.repositories.iuser_repository import IUserRepository
from app.presentation.schemas.user_schema import UserIn, UserDB

from  sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> Iterable[UserDB]:
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()

        return [UserDB.model_validate(user) for user in users]
        
    async def save_user(self, user: UserIn) -> UserDB:
        
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        
        async with self.session as session:
            session.add(db_user)
            await session.commit()
        return UserDB.model_validate(db_user)