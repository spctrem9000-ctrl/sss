from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.admin import AdminLoginRequest, AdminTokenResponse
from app.services.admin import AdminAuthService
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=AdminTokenResponse)
async def login_admin(
    data: AdminLoginRequest,
    db: AsyncSession = Depends(get_db_session)
):
    admin = await AdminAuthService.authenticate(db, data.email, data.password)
    access_token = create_access_token(subject=admin.id)
    return AdminTokenResponse(access_token=access_token, admin=admin)
