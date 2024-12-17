import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.models.base_model import Base
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class TransactionType(enum.Enum):
    SELL = 'Sell'
    RENT = 'Rent'

class PropertyType(enum.Enum):
    HOUSE = 'House'
    APARTMENT = 'Apartment'

class Listing(Base):
    __tablename__ = "listings"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"))
    title: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    area: Mapped[float] = mapped_column()
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType))
    description: Mapped[str] = mapped_column()
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    floor: Mapped[str] = mapped_column()
    num_of_floors: Mapped[str] = mapped_column()
    build_year: Mapped[str] = mapped_column()


