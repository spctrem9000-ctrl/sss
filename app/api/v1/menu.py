from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.menu import MenuResponse
from app.services.menu import menu_service
from app.core.exceptions import BadRequestException

router = APIRouter()

@router.get(
    "",
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Full Menu",
    description="Fetch the complete product catalog for a restaurant, including all active categories and visible products, sized appropriately for building the client UI in one request."
)
async def get_menu(
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    db: AsyncSession = Depends(get_db_session)
):
    if not x_restaurant_id:
        raise BadRequestException("X-Restaurant-ID header is required")
    return await menu_service.get_full_menu(db, x_restaurant_id)
