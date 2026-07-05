from typing import List, Optional
from pydantic import BaseModel, Field

class AppInitializeRequest(BaseModel):
    app_key: str = Field(..., description="The application key configured in the APK")

class BranchInfo(BaseModel):
    id: int
    name: str
    is_default: bool

class RestaurantInfo(BaseModel):
    name: str
    logo_url: Optional[str] = None
    theme_color: Optional[str] = None
    currency: str
    country: str
    default_branch: Optional[BranchInfo] = None
    available_branches: List[BranchInfo]

class AppSettings(BaseModel):
    api_version: str

class AppInitializeResponse(BaseModel):
    restaurant: RestaurantInfo
    settings: AppSettings
