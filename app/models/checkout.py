from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import TimestampModel

class Coupon(TimestampModel):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False, index=True)
    branch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("branches.id"), nullable=True, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False) # percentage, fixed
    discount_value: Mapped[float] = mapped_column(Float, nullable=False)
    min_order: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    max_discount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    usage_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class DeliveryZone(TimestampModel):
    __tablename__ = "delivery_zones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=False)
    zone_name: Mapped[str] = mapped_column(String(255), nullable=False)
    fee: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    min_order: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

class LoyaltyAccount(TimestampModel):
    __tablename__ = "loyalty_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, unique=True)
    points_balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
