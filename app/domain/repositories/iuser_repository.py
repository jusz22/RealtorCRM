from abc import ABC, abstractmethod
from typing import Iterable
from app.presentation.schemas.user_schema import UserIn, UserDB

class IUserRepository(ABC):

    @abstractmethod
    async def get_all_users(self) -> Iterable[UserDB]:
        
        """_summary_
        """

    @abstractmethod 
    async def save_user(self, user: UserIn) -> UserIn:
        """_summary_

        Args:
            UserCreate (_type_): _description_

        Returns:
            UserCreate: _description_
        """
        