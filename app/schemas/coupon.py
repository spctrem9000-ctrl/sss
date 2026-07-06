from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CouponBase(BaseModel):
    restaurant_id: int
    code: str
    discount_type: str
    discount_value: float
    min_order: float = 0.0
    max_discount: Optional[float] = None
    expires_at: Optional[datetime] = None
    usage_limit: Optional[int] = None

class CouponCreate(CouponBase):
    pass

class CouponResponse(CouponBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
