import datetime
from pydantic import UUID4, BaseModel, ConfigDict

from app.infrastructure.models.listing_model import PropertyType, TransactionType


class ListingIn(BaseModel):
    client_id: UUID4
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
    price_per_area: float

class ListingDB(ListingIn):
    id: UUID4
    created_at: datetime.datetime  
    model_config = ConfigDict(from_attributes=True)