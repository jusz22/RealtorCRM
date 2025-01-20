from typing import Iterable
from app.application.interfaces.iclient_service import IClientService
from app.domain.repositories.iclient_repository import IClientRepository
from app.presentation.schemas.client_schema import ClientDB


class ClientService(IClientService):

    _repository: IClientRepository

    def __init__(self, repository: IClientRepository):
        self._repository = repository

    async def add_client(self, client):
        return await self._repository.save_client(client=client)
    
    async def get_all_clients(self) -> Iterable[ClientDB]:
        return await self._repository.get_all_clients()