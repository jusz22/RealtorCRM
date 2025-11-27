from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Factory, Singleton

from app.application.interfaces.services.client_service import ClientService
from app.application.interfaces.services.email_service import EmailService
from app.application.interfaces.services.graph_service import GraphService
from app.application.interfaces.services.listing_service import ListingService
from app.application.interfaces.services.note_service import NoteService
from app.application.interfaces.services.user_service import UserService
from app.infrastructure.db import async_session
from app.infrastructure.repositories.client_repository import ClientRepository
from app.infrastructure.repositories.listing_repository import ListingRepository
from app.infrastructure.repositories.note_repository import NoteRepository
from app.infrastructure.repositories.user_repository import UserRepository


class Container(DeclarativeContainer):
    db = Singleton(lambda: async_session)

    client_repository = Factory(ClientRepository, session=db)

    client_service = Singleton(ClientService, repository=client_repository)

    user_repository = Factory(UserRepository, session=db)

    user_service = Factory(UserService, repository=user_repository)

    listing_repository = Factory(ListingRepository, session=db)

    listing_service = Factory(ListingService, repository=listing_repository)

    note_repository = Factory(NoteRepository, session=db)

    note_service = Factory(NoteService, note_repository=note_repository)

    graph_service = Singleton(GraphService, repository=listing_repository)

    email_service = Singleton(
        EmailService,
        repository=listing_repository,
        graph_service=graph_service,
    )
