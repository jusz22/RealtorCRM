from abc import ABC, abstractmethod
from typing import Iterable, List

class IEmailService(ABC):
    
    @abstractmethod
    async def send_email(self, to: str | List[str], subject: str, html: str):
        """Send email"""
    
    @abstractmethod
    async def get_listing_data(self, listing_id: str) -> Iterable:
        """abstract method"""