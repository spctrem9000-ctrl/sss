from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TimestampModel

class RestaurantHubDevice(TimestampModel):
    __tablename__ = "restaurant_hub_devices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=False, index=True)
    
    device_name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_uuid: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    api_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ACTIVE") # ACTIVE, DISABLED
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant")
    branch: Mapped["Branch"] = relationship("Branch")
