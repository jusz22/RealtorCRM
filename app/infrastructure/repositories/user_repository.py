from typing import Iterable

from sqlalchemy import select

from app.infrastructure.models.user_model import User
from app.domain.repositories.iuser_repository import IUserRepository
from app.presentation.schemas.user_schema import UserInDB

from  sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> Iterable[UserInDB]:
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()

        return [UserInDB.model_validate(user) for user in users]
        