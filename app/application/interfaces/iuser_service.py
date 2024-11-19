from abc import ABC, abstractmethod
from typing import Iterable

from app.presentation.schemas.user_schema import UserCreate, UserInDB

class IUserService(ABC):
    
    @abstractmethod
    async def get_all(self) -> Iterable[UserInDB]:
        """_summary_

        Returns:
            Iterable[UserInDB]: _description_
        """

    @abstractmethod
    async def save_user(self, user: UserCreate) -> UserCreate:
        """_summary_

        Returns:
            UserCreate: _description_
        """

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> UserCreate | None:
        pass