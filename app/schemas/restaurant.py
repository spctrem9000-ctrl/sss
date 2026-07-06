from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class RestaurantBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    theme_color: Optional[str] = None
    currency: str = "SAR"
    country: str = "SA"
    is_enabled: bool = True
    settings: Optional[Dict[str, Any]] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    theme_color: Optional[str] = None
    currency: Optional[str] = None
    country: Optional[str] = None
    is_enabled: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
