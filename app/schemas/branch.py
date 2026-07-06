from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class BranchBase(BaseModel):
    restaurant_id: int
    name: str
    is_enabled: bool = True
    is_default: bool = False
    settings: Optional[Dict[str, Any]] = None

class BranchCreate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
