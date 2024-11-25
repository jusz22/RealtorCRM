from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from app.infrastructure.repositories.user_repository import \
    UserRepository
from app.application.interfaces.services.user_service import UserService
from app.infrastructure.db import async_session


class Container(DeclarativeContainer):
    db = Singleton(async_session)
    
    user_repository = Factory(
    UserRepository,
    session = db)

    user_service = Factory(
        UserService,
        repository=user_repository,
    )

