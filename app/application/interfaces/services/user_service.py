from typing import Iterable
from app.application.interfaces.iuser_service import IUserService
from app.domain.repositories.iuser_repository import IUserRepository
from app.infrastructure.security import verify_password
from app.presentation.schemas.user_schema import UserCreate, UserInDB


class UserService(IUserService):

    _repository = IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def get_all(self) -> Iterable[UserInDB]:
        return await self._repository.get_all_users()
    
    async def save_user(self, user: UserCreate) -> UserCreate:
        return await self._repository.save_user(user)
    
    async def authenticate_user(self, username: str, password: str) -> UserCreate | None:
        user = await self._repository.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user