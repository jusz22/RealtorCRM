from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from app.application.interfaces.services.email_service import EmailService
from app.application.interfaces.services.listing_service import ListingService
from app.infrastructure.repositories.listing_repository import ListingRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.interfaces.services.user_service import UserService
from app.infrastructure.db import async_session

from app.infrastructure.config import config

class Container(DeclarativeContainer):
    db = Singleton(async_session)

    email_service = Singleton(
        EmailService,
        API_KEY = config.RESEND_API_KEY)
    
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

