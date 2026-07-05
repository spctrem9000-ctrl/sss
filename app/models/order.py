from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, Integer, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import TimestampModel

class Order(TimestampModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=False)
    coupon_id: Mapped[Optional[int]] = mapped_column(ForeignKey("coupons.id"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="NEW")
    
    subtotal: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    addons_total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    discount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    delivery_fee: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    tax: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    estimated_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    history: Mapped[List["OrderStatusHistory"]] = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")


class OrderItem(TimestampModel):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    size_id: Mapped[Optional[int]] = mapped_column(ForeignKey("product_sizes.id"), nullable=True)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    addons_total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    addons: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="items")


class OrderStatusHistory(TimestampModel):
    __tablename__ = "order_status_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    old_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # customer_id or user_id

    order: Mapped["Order"] = relationship("Order", back_populates="history")
