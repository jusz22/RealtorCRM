import datetime
from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict

from app.infrastructure.models.listing_model import PropertyType, TransactionType


class ListingIn(BaseModel):
    client_id: Optional[UUID4] = None
    title: str
    location: str
    street: str
    price: int
    area: float
    property_type: PropertyType
    description: str 
    transaction_type: TransactionType
    floor: str
    num_of_floors: str 
    build_year: str

class ListingDB(ListingIn):
    id: UUID4
    created_at: datetime.datetime  
    price_per_area: float
    model_config = ConfigDict(from_attributes=True)