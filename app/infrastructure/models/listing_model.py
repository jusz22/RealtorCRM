import enum
from app.infrastructure.models.base_model import Base
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

class TransactionType(enum.Enum):
    SELL = 'Sell'
    RENT = 'Rent'

class PropertyType(enum.Enum):
    HOUSE = 'House'
    APARTMENT = 'Apartment'

class Listing(Base):
    __tablename__ = "listings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    area: Mapped[float] = mapped_column()
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType))
    description: Mapped[str] = mapped_column()
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))


