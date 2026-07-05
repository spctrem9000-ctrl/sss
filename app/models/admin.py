from typing import Optional
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TimestampModel

class AdminUser(TimestampModel):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="RESTAURANT_ADMIN") # SUPER_ADMIN, RESTAURANT_ADMIN
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    restaurant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("restaurants.id"), nullable=True, index=True)

    restaurant: Mapped[Optional["Restaurant"]] = relationship("Restaurant")
