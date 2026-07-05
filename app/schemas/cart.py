from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.menu import ProductResponse, ProductSizeResponse

class CartItemAddRequest(BaseModel):
    product_id: int
    size_id: Optional[int] = None
    quantity: int = Field(default=1, gt=0)
    notes: Optional[str] = None
    addons: Optional[List[int]] = None # List of Addon IDs

class CartItemUpdateRequest(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None
    addons: Optional[List[int]] = None

class CartItemUpdateQuantityRequest(BaseModel):
    quantity: int = Field(..., gt=0)

class ApplyCouponRequest(BaseModel):
    code: str

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    size_id: Optional[int] = None
    quantity: int
    unit_price: float
    addons_total: float = 0.0
    total_price: float
    notes: Optional[str] = None
    addons: Optional[List[int]] = None
    
    product: Optional[ProductResponse] = None
    size: Optional[ProductSizeResponse] = None

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    restaurant_id: int
    customer_id: int
    branch_id: Optional[int] = None
    coupon_id: Optional[int] = None
    status: str
    subtotal: float
    addons_total: float = 0.0
    discount: float
    delivery_fee: float
    tax: float
    total: float
    
    items: List[CartItemResponse] = []
    
    coupons_applied: List[str] = [] # Display only
    loyalty_used: float = 0.0 # Display only

    class Config:
        from_attributes = True
