from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class HeartbeatRequest(BaseModel):
    version: str
    device_name: str

class OrderStatusUpdateRequest(BaseModel):
    status: str

class HubSettingsResponse(BaseModel):
    restaurant_settings: Optional[Dict[str, Any]] = None
    branch_settings: Optional[Dict[str, Any]] = None

class HubDeviceResponse(BaseModel):
    id: int
    restaurant_id: int
    branch_id: int
    device_name: str
    status: str
    version: Optional[str] = None
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True
