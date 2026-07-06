from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db_session
from app.models.admin import AdminUser
from app.models.menu import Category, Product
from app.schemas.menu import CategoryResponse, ProductResponse
from app.api.deps import get_current_admin
from app.core.exceptions import UnauthorizedException
from pydantic import BaseModel

router = APIRouter()

class CategoryCreateAdmin(BaseModel):
    restaurant_id: int
    name_ar: str
    name_en: str
    image: str = None
    sort_order: int = 0
    is_active: bool = True

class ProductCreateAdmin(BaseModel):
    restaurant_id: int
    category_id: int
    name_ar: str
    name_en: str
    description_ar: str = None
    description_en: str = None
    base_price: float
    is_available: bool = True
    sort_order: int = 0

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreateAdmin,
    admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_session)
):
    if admin.role != "SUPER_ADMIN" and admin.restaurant_id != data.restaurant_id:
        raise UnauthorizedException("Cannot create category for another restaurant")
        
    category = Category(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreateAdmin,
    admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_session)
):
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product
