from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.base import TimestampSchema

class OTPRequest(BaseModel):
    phone_number: str = Field(..., description="Customer's phone number")

class OTPVerifyRequest(BaseModel):
    phone_number: str = Field(..., description="Customer's phone number")
    code: str = Field(..., description="6-digit OTP code")

class CustomerProfile(TimestampSchema):
    id: int
    phone_number: str
    name: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    customer: CustomerProfile
