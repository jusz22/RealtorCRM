from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from app.application.interfaces.services.client_service import ClientService
from app.application.interfaces.services.email_service import EmailService
from app.application.interfaces.services.listing_service import ListingService
from app.infrastructure.repositories.client_repository import ClientRepository
from app.infrastructure.repositories.listing_repository import ListingRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.interfaces.services.user_service import UserService
from app.infrastructure.db import async_session

class Container(DeclarativeContainer):
    db = Singleton(async_session)


    client_repository = Singleton(
        ClientRepository,
        session = db
    )
    
    client_service = Singleton(
        ClientService,
        repository = client_repository
    )

    user_repository = Factory(
        UserRepository,
        session = db
    )

    user_service = Factory(
        UserService,
        repository = user_repository
    )

    listing_repository = Factory(
        ListingRepository,
        session = db
    )
    listing_service = Factory(
        ListingService,
        repository = listing_repository
    )
    
    email_service = Singleton(
        EmailService,
        repository = listing_repository)

