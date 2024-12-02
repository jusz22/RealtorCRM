from sqlalchemy import ForeignKey, LargeBinary
from app.infrastructure.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column

class ListingPhoto(Base):
    __tablename__ = "listing_photos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    image_data: Mapped[LargeBinary] = mapped_column()