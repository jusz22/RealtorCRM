from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.application.interfaces.iclient_service import IClientService
from app.container import Container
from app.application.interfaces.iemail_service import IEmailService
from app.presentation.schemas.client_schema import ClientDB, ClientIn

router = APIRouter()


@router.post("/email")
@inject
async def send_email(
    email_address: str,
    email_service: IEmailService = Depends(Provide[Container.email_service])
):
    result = await email_service.send_email(to=email_address, subject="Test", html="<h1>Hello</h1>")

    return result

@router.post("/clients")
@inject
async def add_client(
    client: ClientIn,
    service: IClientService = Depends(Provide[Container.client_service])
) -> ClientDB:
        return await service.add_client(client=client)
    