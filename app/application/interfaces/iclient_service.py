from abc import ABC, abstractmethod

from app.presentation.schemas.client_schema import ClientDB, ClientIn

class IClientService(ABC):

    @abstractmethod
    async def add_client(self, client: ClientIn) -> ClientDB:
        """abstract method"""