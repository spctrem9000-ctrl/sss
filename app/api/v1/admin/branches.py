from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database.session import get_db_session
from app.models.admin import AdminUser
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchResponse
from app.api.deps import get_current_admin
from app.core.exceptions import UnauthorizedException

router = APIRouter()

@router.post("", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
async def create_branch(
    data: BranchCreate,
    admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_session)
):
    if admin.role != "SUPER_ADMIN" and admin.restaurant_id != data.restaurant_id:
        raise UnauthorizedException("Cannot create branch for another restaurant")
        
    branch = Branch(**data.model_dump())
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch

@router.get("", response_model=List[BranchResponse])
async def get_branches(
    restaurant_id: int = None,
    admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_session)
):
    stmt = select(Branch)
    if admin.role != "SUPER_ADMIN":
        stmt = stmt.filter(Branch.restaurant_id == admin.restaurant_id)
    elif restaurant_id:
        stmt = stmt.filter(Branch.restaurant_id == restaurant_id)
        
    result = await db.execute(stmt)
    return result.scalars().all()
