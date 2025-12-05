import datetime
import enum
import uuid
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.models.base_model import Base
from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

class TransactionType(enum.Enum):
    SELL = 'Sell'
    RENT = 'Rent'

class PropertyType(enum.Enum):
    HOUSE = 'House'
    APARTMENT = 'Apartment'

class Listing(Base):
    __tablename__ = "listings"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    client_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    area: Mapped[float] = mapped_column()
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType))
    description: Mapped[str] = mapped_column()
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    floor: Mapped[str] = mapped_column()
    num_of_floors: Mapped[str] = mapped_column()
    build_year: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.current_timestamp(), nullable=False)
    
    @hybrid_property
    def price_per_area(self) -> float:
        if self.area and self.area != 0:
            return round(self.price / self.area)
        return 0.0
