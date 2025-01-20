from abc import ABC, abstractmethod
from typing import Iterable

from app.presentation.schemas.client_schema import ClientDB, ClientIn

class IClientRepository(ABC):
    @abstractmethod
    async def save_client(self, client: ClientIn) -> ClientDB:
        """abstract method"""

    @abstractmethod
    async def get_all_clients(self) -> Iterable[ClientDB]:
        """abstract method"""