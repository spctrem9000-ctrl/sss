from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database.session import get_db_session
from app.models.admin import AdminUser
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse
from app.api.deps import require_super_admin, get_current_admin

router = APIRouter()

@router.post("", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    data: RestaurantCreate,
    admin: AdminUser = Depends(require_super_admin),
    db: AsyncSession = Depends(get_db_session)
):
    restaurant = Restaurant(**data.model_dump())
    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant

@router.get("", response_model=List[RestaurantResponse])
async def get_restaurants(
    admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_session)
):
    if admin.role == "SUPER_ADMIN":
        stmt = select(Restaurant)
    else:
        stmt = select(Restaurant).filter(Restaurant.id == admin.restaurant_id)
        
    result = await db.execute(stmt)
    return result.scalars().all()

from fastapi import HTTPException
from app.schemas.restaurant import RestaurantUpdate

@router.patch("/{id}", response_model=RestaurantResponse)
async def update_restaurant(
    id: int,
    data: RestaurantUpdate,
    admin: AdminUser = Depends(require_super_admin),
    db: AsyncSession = Depends(get_db_session)
):
    stmt = select(Restaurant).filter(Restaurant.id == id)
    result = await db.execute(stmt)
    restaurant = result.scalars().first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
        
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(restaurant, key, value)
        
    await db.commit()
    await db.refresh(restaurant)
    return restaurant
