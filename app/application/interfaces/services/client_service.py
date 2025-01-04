from app.application.interfaces.iclient_service import IClientService
from app.domain.repositories.iclient_repository import IClientRepository


class ClientService(IClientService):

    _repository: IClientRepository

    def __init__(self, repository: IClientRepository):
        self._repository = repository

    async def add_client(self, client):
        return await self._repository.save_client(client=client)