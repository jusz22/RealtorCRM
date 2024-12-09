from pydantic import UUID4, BaseModel

from app.infrastructure.models.listing_model import PropertyType, TransactionType


class ListingIn(BaseModel):
    title: str 
    location: str 
    street: str 
    price: str 
    area: float 
    property_type: PropertyType
    description: str 
    transaction_type: TransactionType
    floor: str
    num_of_floors: str 
    build_year: str    


class ListingDB(ListingIn):
    id: UUID4