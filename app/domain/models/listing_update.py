from pydantic import BaseModel
from typing import Optional
import datetime

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    client_id: Optional[str] = None
    location: Optional[str] = None
    street: Optional[str] = None
    price: Optional[int] = None
    area: Optional[float] = None
    property_type: Optional[str] = None
    description: Optional[str] = None
    transaction_type: Optional[str] = None
    floor: Optional[str] = None
    num_of_floors: Optional[str] = None
    build_year: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
