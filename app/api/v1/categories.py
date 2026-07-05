from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.menu import Page, CategoryResponse
from app.services.menu import menu_service
from app.core.exceptions import BadRequestException

router = APIRouter()

@router.get(
    "",
    response_model=Page[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Categories",
    description="Fetch a paginated list of active categories for the given restaurant."
)
async def get_categories(
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    db: AsyncSession = Depends(get_db_session)
):
    if not x_restaurant_id:
        raise BadRequestException("X-Restaurant-ID header is required")
    return await menu_service.get_categories(db, x_restaurant_id, skip=skip, limit=limit)

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Category Details"
)
async def get_category(
    category_id: int,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    db: AsyncSession = Depends(get_db_session)
):
    return await menu_service.get_category(db, category_id, x_restaurant_id)
