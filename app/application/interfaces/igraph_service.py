from abc import ABC, abstractmethod
from io import BytesIO

class IGraphService(ABC):

    @abstractmethod
    async def generate_graph_buffer(self, year_or_all: int | None = None) -> BytesIO:
        """abstract method"""