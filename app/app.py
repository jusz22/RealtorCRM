from app.infrastructure.db import database
from app.infrastructure.db import init_db

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.infrastructure.config import config
from app.presentation.api.v1.routes.listing_route import router as listing_router
from app.presentation.api.v1.routes.auth.jwt import router as jwt_router
from app.presentation.api.v1.routes.user_route import router as user_router
from app.presentation.api.v1.routes.client_router import router as client_router
from app.presentation.api.v1.routes.graph_router import router as graph_router
from app.container import Container
from fastapi import FastAPI

container = Container()
container.wire(modules=[
    "app.presentation.api.v1.routes.user_route",
    "app.presentation.api.v1.routes.auth.jwt",
    "app.infrastructure.security",
    "app.presentation.api.v1.routes.listing_route",
    "app.presentation.api.v1.routes.client_router",
    "app.presentation.api.v1.routes.graph_router"
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix=config.API_STR)
app.include_router(jwt_router, prefix=config.API_STR, dependencies=[])
app.include_router(listing_router, prefix=config.API_STR)
app.include_router(client_router, prefix=config.API_STR)
app.include_router(graph_router, prefix=config.API_STR)
