from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.auth import OTPRequest, OTPVerifyRequest, TokenResponse
from app.services.auth import auth_service

router = APIRouter()

@router.post(
    "/request-otp",
    status_code=status.HTTP_200_OK,
    summary="Request OTP",
    description="Generates and sends a 6-digit OTP to the customer's phone number.",
    responses={
        200: {"description": "OTP generated successfully"}
    }
)
async def request_otp(
    request: OTPRequest,
    db: AsyncSession = Depends(get_db_session)
):
    await auth_service.request_otp(db, request.phone_number)
    return {"message": "OTP sent successfully"}

@router.post(
    "/verify-otp",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP and Login",
    description="Verifies the OTP. If valid, logs in the customer and returns JWT tokens. Creates a new customer if they do not exist.",
    responses={
        200: {"description": "Successful Login"},
        400: {"description": "Invalid or expired OTP"}
    }
)
async def verify_otp(
    request: OTPVerifyRequest,
    db: AsyncSession = Depends(get_db_session)
):
    return await auth_service.verify_otp(db, request.phone_number, request.code)
