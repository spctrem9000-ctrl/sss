from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.customer import customer_repo, CustomerCreate
from app.repositories.otp import otp_repo, OtpCreate
from app.repositories.token import token_repo, TokenCreate
from app.schemas.auth import TokenResponse, CustomerProfile
from app.core.security import generate_otp, create_access_token, generate_refresh_token, get_token_hash
from app.core.config import settings
from app.core.exceptions import BadRequestException
from loguru import logger

class AuthService:
    async def request_otp(self, db: AsyncSession, phone_number: str) -> None:
        logger.info(f"OTP requested for phone: {phone_number}")
        
        # Clean up existing OTPs for phone
        await otp_repo.delete_by_phone(db, phone_number)
        
        # Generate new OTP (fake send for now)
        code = generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        await otp_repo.create(db, obj_in=OtpCreate(
            phone_number=phone_number,
            code=code,
            expires_at=expires_at
        ))
        
        logger.info(f"Generated OTP {code} for phone {phone_number}")
        # In a real scenario, integrate SMS provider here.

    async def verify_otp(self, db: AsyncSession, phone_number: str, code: str) -> TokenResponse:
        logger.info(f"Verifying OTP for phone: {phone_number}")
        
        # 1. Validate OTP
        valid_otp = await otp_repo.get_valid_otp(db, phone_number, code)
        if not valid_otp:
            logger.error(f"Invalid or expired OTP for phone: {phone_number}")
            raise BadRequestException("Invalid or expired OTP")
            
        # 2. Delete OTP
        await otp_repo.delete_by_phone(db, phone_number)
        
        # 3. Get or Create Customer
        customer = await customer_repo.get_by_phone(db, phone_number)
        if not customer:
            logger.info(f"Creating new customer for phone: {phone_number}")
            customer = await customer_repo.create(db, obj_in=CustomerCreate(phone_number=phone_number))
        else:
            if not customer.is_active:
                logger.error(f"Customer {customer.id} is disabled")
                raise BadRequestException("Customer account is disabled")
            logger.info(f"Customer {customer.id} logged in")
            
        # 4. Generate Tokens
        access_token = create_access_token(subject=customer.id)
        refresh_token_plain = generate_refresh_token()
        refresh_token_hash = get_token_hash(refresh_token_plain)
        
        refresh_expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Store refresh token
        await token_repo.create(db, obj_in=TokenCreate(
            customer_id=customer.id,
            token_hash=refresh_token_hash,
            expires_at=refresh_expires
        ))
        
        profile = CustomerProfile.model_validate(customer)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_plain,
            customer=profile
        )

auth_service = AuthService()
