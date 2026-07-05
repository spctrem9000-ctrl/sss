from typing import Optional
from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.menu import Page, ProductResponse
from app.services.menu import menu_service
from app.core.exceptions import BadRequestException

router = APIRouter()

@router.get(
    "",
    response_model=Page[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Products",
    description="Fetch a paginated list of products for the given restaurant, supporting searching and filtering."
)
async def get_products(
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    category_id: Optional[int] = Query(None, description="Filter by Category ID"),
    available_only: bool = Query(True, description="Return only available products"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    is_offer: Optional[bool] = Query(None, description="Filter by offer status"),
    search: Optional[str] = Query(None, description="Search term (Arabic or English)"),
    sort_by: str = Query("sort_order", description="Sort field: sort_order, price_asc, price_desc, newest"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    db: AsyncSession = Depends(get_db_session)
):
    if not x_restaurant_id:
        raise BadRequestException("X-Restaurant-ID header is required")
        
    return await menu_service.get_products(
        db, 
        restaurant_id=x_restaurant_id, 
        category_id=category_id,
        available_only=available_only,
        is_featured=is_featured,
        is_offer=is_offer,
        search_query=search,
        sort_by=sort_by,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Product Details",
    description="Get the full product details including sizes and addons."
)
async def get_product(
    product_id: int,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    db: AsyncSession = Depends(get_db_session)
):
    return await menu_service.get_product(db, product_id, x_restaurant_id)
