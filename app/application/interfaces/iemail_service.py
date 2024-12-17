from abc import ABC, abstractmethod
from typing import List

class IEmailService(ABC):
    @abstractmethod
    async def send_email(self, to: str | List[str], subject: str, html: str):
        """Send email"""