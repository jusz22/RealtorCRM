from typing import Iterable

from sqlalchemy import select
from app.application.interfaces.iuser_service import IUserService
from app.domain.dtos.sort_options_dto import SortOptions
from app.domain.repositories.iuser_repository import IUserRepository
from app.infrastructure.models.user_model import User
from app.presentation.schemas.user_schema import UserIn, UserDB



class UserService(IUserService):

    _repository = IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def get_all(self, sort_options: SortOptions) -> Iterable[UserDB]:
        query = select(User)
        sort_func = sort_options.get_sort_func()

        if sort_func is not None:
            query = query.order_by(sort_func)
        
        return await self._repository.get_all_users(query=query)
    
    async def save_user(self, user: UserIn) -> UserIn:
        return await self._repository.save_user(user=user)

    async def get_user(self, user_id) -> UserDB | None:
        return await self._repository.get_user(user_id=user_id)
    
    async def delete_user(self, user_id) -> UserDB | None:
        return await self._repository.delete_user(user_id=user_id)