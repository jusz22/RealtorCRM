from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import delete


from app.presentation.schemas.user_schema import UserIn, UserDB


class IUserService(ABC):
    
    @abstractmethod
    async def get_all(self) -> Iterable[UserDB]:
        """_summary_

        Returns:
            Iterable[UserInDB]: _description_
        """

    @abstractmethod
    async def save_user(self, user: UserIn) -> UserIn:
        """_summary_

        Returns:
            UserCreate: _description_
        """

    @abstractmethod
    async def get_user(self, user_id) -> UserDB | None:
        """abstract method"""

    @abstractmethod
    async def delete_user(self, user_id) -> UserDB | None:
        """abstract method"""