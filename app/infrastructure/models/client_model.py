from app.infrastructure.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column

import uuid
from sqlalchemy.dialects.postgresql import UUID

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
