from abc import ABC, abstractmethod
from typing import Iterable

from app.presentation.schemas.user_schema import UserInDB

class IUserService(ABC):
    
    @abstractmethod
    async def get_all(self) -> Iterable[UserInDB]:
        """_summary_

        Returns:
            Iterable[UserInDB]: _description_
        """
