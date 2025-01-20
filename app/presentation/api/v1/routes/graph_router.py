from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import Provide, inject
from fastapi.responses import StreamingResponse

from app.application.interfaces.igraph_service import IGraphService
from app.container import Container


router = APIRouter()

@router.get("/graph")
@inject
async def get_graph(
    graph_service: IGraphService = Depends(Provide[Container.graph_service]),
    year: Annotated[int | None, 
        Query(description="""Optional query parameter. Pass a year to display that years summary of prices. 
            If nothing is passed it defaults to whats in the database.""")] = None
):
    img = await graph_service.generate_graph_buffer(year_or_all=year)
    return StreamingResponse(img, media_type="image/png")