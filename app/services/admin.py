from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.admin import AdminUser
from app.core.security import verify_password, get_password_hash
from app.core.exceptions import UnauthorizedException, BadRequestException

class AdminAuthService:
    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> AdminUser:
        stmt = select(AdminUser).filter(AdminUser.email == email)
        result = await db.execute(stmt)
        admin = result.scalars().first()
        
        if not admin:
            raise UnauthorizedException("Invalid credentials")
            
        if not verify_password(password, admin.hashed_password):
            raise UnauthorizedException("Invalid credentials")
            
        if not admin.is_active:
            raise UnauthorizedException("Account is inactive")
            
        return admin

    @staticmethod
    async def create_admin(db: AsyncSession, email: str, password: str, first_name: str, last_name: str, role: str = "RESTAURANT_ADMIN", restaurant_id: int = None) -> AdminUser:
        stmt = select(AdminUser).filter(AdminUser.email == email)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise BadRequestException("Email already registered")
            
        admin = AdminUser(
            email=email,
            hashed_password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role=role,
            restaurant_id=restaurant_id
        )
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        return admin
