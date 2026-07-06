from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.menu import ProductResponse, ProductSizeResponse

class CheckoutRequest(BaseModel):
    payment_method: str
    delivery_zone_id: Optional[int] = None
    notes: Optional[str] = None

class OrderStatusHistoryResponse(BaseModel):
    id: int
    old_status: Optional[str] = None
    new_status: str
    created_at: datetime
    created_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    size_id: Optional[int] = None
    quantity: int
    unit_price: float
    addons_total: float
    total_price: float
    notes: Optional[str] = None
    addons: Optional[list] = None
    
    product: Optional[ProductResponse] = None
    size: Optional[ProductSizeResponse] = None

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    subtotal: float
    addons_total: float
    discount: float
    delivery_fee: float
    tax: float
    total: float
    payment_method: str
    estimated_time: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderDetailResponse(OrderResponse):
    restaurant_id: int
    branch_id: int
    customer_id: int
    coupon_id: Optional[int] = None
    
    items: List[OrderItemResponse] = []
    history: List[OrderStatusHistoryResponse] = []
