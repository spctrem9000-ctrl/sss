from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AdminUserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    restaurant_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: AdminUserResponse
