from abc import ABC, abstractmethod
from typing import Iterable
from app.presentation.schemas.user_schema import UserCreate, UserInDB

class IUserRepository(ABC):

    @abstractmethod
    async def get_all_users(self) -> Iterable[UserInDB]:
        
        """_summary_
        """

    @abstractmethod 
    async def save_user(self, user: UserCreate) -> UserCreate:
        """_summary_

        Args:
            UserCreate (_type_): _description_

        Returns:
            UserCreate: _description_
        """

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserCreate:
        """_summary_

        Args:
            username (str): _description_
        """