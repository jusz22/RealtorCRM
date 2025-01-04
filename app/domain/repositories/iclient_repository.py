from abc import ABC, abstractmethod

from app.presentation.schemas.client_schema import ClientDB, ClientIn

class IClientRepository(ABC):
    @abstractmethod
    async def save_client(self, client: ClientIn) -> ClientDB:
        """abstract method"""