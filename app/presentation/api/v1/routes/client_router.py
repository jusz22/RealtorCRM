from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.container import Container
from app.application.interfaces.iemail_service import IEmailService

router = APIRouter()


@router.post("/email")
@inject
async def send_email(
    email_address: str,
    email_service: IEmailService = Depends(Provide[Container.email_service])
):
    result = await email_service.send_email(to=email_address, subject="Test", html="<h1>Hello</h1>")

    return result