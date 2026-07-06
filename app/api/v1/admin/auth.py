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

@router.post("/setup", response_model=AdminTokenResponse)
async def setup_super_admin(
    data: AdminLoginRequest,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        from sqlalchemy import select
        from app.models.admin import AdminUser
        
        # Check if any super admin exists
        stmt = select(AdminUser).filter(AdminUser.role == "SUPER_ADMIN")
        result = await db.execute(stmt)
        if result.scalars().first():
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Super admin already exists. Setup is locked.")
            
        # Create the first super admin
        admin = await AdminAuthService.create_admin(
            db=db,
            email=data.email,
            password=data.password,
            first_name="Super",
            last_name="Admin",
            role="SUPER_ADMIN"
        )
        
        access_token = create_access_token(subject=admin.id)
        return AdminTokenResponse(access_token=access_token, admin=admin)
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        err_msg = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=err_msg)
