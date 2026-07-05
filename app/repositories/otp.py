from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.otp import OtpCode
from pydantic import BaseModel

class OtpCreate(BaseModel):
    phone_number: str
    code: str
    expires_at: datetime

class OtpRepository(BaseRepository[OtpCode, OtpCreate, BaseModel]):
    def __init__(self):
        super().__init__(OtpCode)

    async def get_valid_otp(self, db: AsyncSession, phone_number: str, code: str) -> Optional[OtpCode]:
        stmt = select(OtpCode).filter(
            OtpCode.phone_number == phone_number,
            OtpCode.code == code,
            OtpCode.expires_at > datetime.now(timezone.utc)
        )
        result = await db.execute(stmt)
        return result.scalars().first()
    
    async def delete_by_phone(self, db: AsyncSession, phone_number: str) -> None:
        await db.execute(delete(OtpCode).filter(OtpCode.phone_number == phone_number))
        await db.commit()

otp_repo = OtpRepository()
