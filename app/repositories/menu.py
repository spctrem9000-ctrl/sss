from typing import List, Optional, Tuple
from sqlalchemy import select, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.models.menu import Category, Product, ProductImage, ProductSize, AddonGroup, Addon
from pydantic import BaseModel

class CategoryRepository(BaseRepository[Category, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Category)

    async def get_active_categories(self, db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[Category], int]:
        stmt = select(Category).filter(
            Category.restaurant_id == restaurant_id,
            Category.is_active == True
        )
        
        # Count total
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt) or 0
        
        # Fetch items
        stmt = stmt.order_by(Category.sort_order).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all()), total


class ProductRepository(BaseRepository[Product, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Product)

    async def get_products(
        self, 
        db: AsyncSession, 
        restaurant_id: int,
        category_id: Optional[int] = None,
        available_only: bool = True,
        is_featured: Optional[bool] = None,
        is_offer: Optional[bool] = None,
        search_query: Optional[str] = None,
        sort_by: str = "sort_order",
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[Product], int]:
        stmt = select(Product).filter(
            Product.restaurant_id == restaurant_id,
            Product.is_hidden == False
        )
        
        if available_only:
            stmt = stmt.filter(Product.is_available == True)
            
        if category_id is not None:
            stmt = stmt.filter(Product.category_id == category_id)
            
        if is_featured is not None:
            stmt = stmt.filter(Product.is_featured == is_featured)
            
        if is_offer is not None:
            stmt = stmt.filter(Product.is_offer == is_offer)
            
        if category_id:
            stmt = stmt.filter(Product.category_id == category_id)
            
        if search_query:
            search_term = f"%{search_query}%"
            stmt = stmt.filter(
                or_(
                    Product.name_ar.ilike(search_term),
                    Product.name_en.ilike(search_term)
                )
            )

        # Count total
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt) or 0
        
        # Apply Sorting
        if sort_by == "price_asc":
            stmt = stmt.order_by(asc(Product.base_price))
        elif sort_by == "price_desc":
            stmt = stmt.order_by(desc(Product.base_price))
        elif sort_by == "newest":
            stmt = stmt.order_by(desc(Product.created_at))
        else:
            stmt = stmt.order_by(Product.sort_order)
            
        # Eager load relationships
        stmt = stmt.options(
            selectinload(Product.images),
            selectinload(Product.sizes),
            selectinload(Product.addon_groups).selectinload(AddonGroup.addons)
        )

        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all()), total

    async def get_product_details(self, db: AsyncSession, product_id: int, restaurant_id: int) -> Optional[Product]:
        stmt = select(Product).filter(
            Product.id == product_id,
            Product.restaurant_id == restaurant_id
        ).options(
            selectinload(Product.images),
            selectinload(Product.sizes),
            selectinload(Product.addon_groups).selectinload(AddonGroup.addons)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_all_menu_products(self, db: AsyncSession, restaurant_id: int) -> List[Product]:
        stmt = select(Product).filter(
            Product.restaurant_id == restaurant_id,
            Product.is_hidden == False
        ).order_by(Product.sort_order).options(
            selectinload(Product.images),
            selectinload(Product.sizes),
            selectinload(Product.addon_groups).selectinload(AddonGroup.addons)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

category_repo = CategoryRepository()
product_repo = ProductRepository()
