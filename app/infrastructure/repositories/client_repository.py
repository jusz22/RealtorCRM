from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.iclient_repository import IClientRepository
from app.infrastructure.models.client_model import Client
from app.presentation.schemas.client_schema import ClientDB, ClientIn


class ClientRepository(IClientRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_client(self, client: ClientIn):
        
        db_client = Client(**client.model_dump())
        
        async with self._session as session:
            session.add(db_client)
            await session.commit()
            await session.refresh(db_client)
            
            return ClientDB(
                id=db_client.id,
                **client.model_dump())