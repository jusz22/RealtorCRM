from app.infrastructure.db import database
from app.infrastructure.db import init_db

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.presentation.api.v1.routes.user_route import router as user_router
from app.container import Container
from fastapi import FastAPI

container = Container()
container.wire(modules=[
    "app.presentation.api.v1.routes.user_route",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/api/v1")