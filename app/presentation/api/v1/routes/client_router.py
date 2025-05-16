from typing import Iterable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.application.interfaces.iclient_service import IClientService
from app.application.interfaces.iemail_service import IEmailService
from app.container import Container
from app.infrastructure.security import verify_token
from app.presentation.schemas.client_schema import ClientDB, ClientIn

router = APIRouter(dependencies=[Depends(verify_token)])


@router.post("/email")
@inject
async def send_email(
    email_address: EmailStr,
    listing_id: str,
    email_service: IEmailService = Depends(Provide[Container.email_service]),
):
    try:
        return await email_service.send_email(
            to=email_address, subject="Listing", listing_id=listing_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Couldn't send the email {str(e)}",
        )


@router.post("/clients")
@inject
async def add_client(
    client: ClientIn,
    service: IClientService = Depends(Provide[Container.client_service]),
) -> ClientDB:
    return await service.add_client(client=client)


@router.get("/clients")
@inject
async def get_all_clients(
    service: IClientService = Depends(Provide[Container.client_service]),
) -> Iterable[ClientDB]:
    return await service.get_all_clients()
