from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database.session import get_db_session
from app.models.admin import AdminUser
from app.schemas.admin import AdminCreateRequest, AdminUserResponse
from app.api.deps import require_super_admin
from app.services.admin import AdminAuthService

router = APIRouter()

@router.get("", response_model=List[AdminUserResponse])
async def get_admins(
    admin: AdminUser = Depends(require_super_admin),
    db: AsyncSession = Depends(get_db_session)
):
    stmt = select(AdminUser).filter(AdminUser.role != "SUPER_ADMIN")
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(
    data: AdminCreateRequest,
    admin: AdminUser = Depends(require_super_admin),
    db: AsyncSession = Depends(get_db_session)
):
    # Check if email exists
    stmt = select(AdminUser).filter(AdminUser.email == data.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_admin = await AdminAuthService.create_admin(
        db=db,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        role="RESTAURANT_ADMIN",
        restaurant_id=data.restaurant_id
    )
    return new_admin
