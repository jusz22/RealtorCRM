from abc import ABC, abstractmethod
from typing import Iterable

from app.presentation.schemas.client_schema import ClientDB, ClientIn

class IClientService(ABC):

    @abstractmethod
    async def add_client(self, client: ClientIn) -> ClientDB:
        """abstract method"""

    @abstractmethod
    async def get_all_clients(self) -> Iterable[ClientDB]:
        """abstract method"""