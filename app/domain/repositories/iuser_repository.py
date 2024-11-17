from abc import ABC, abstractmethod
from typing import Iterable
from app.presentation.schemas.user_schema import UserInDB

class IUserRepository(ABC):

    @abstractmethod
    async def get_all_users(self) -> Iterable[UserInDB]:
        
        """_summary_
        """