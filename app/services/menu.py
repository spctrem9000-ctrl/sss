from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.menu import category_repo, product_repo
from app.schemas.menu import Page, CategoryResponse, ProductResponse, AddonGroupResponse, ProductSizeResponse
from app.core.cache import cache
from app.core.exceptions import NotFoundException
from loguru import logger
import math

class MenuService:
    async def get_categories(self, db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 100) -> Page[CategoryResponse]:
        cache_key = f"categories:rest_{restaurant_id}:skip_{skip}:limit_{limit}"
        cached_result = await cache.get(cache_key)
        if cached_result:
            return cached_result
            
        categories, total = await category_repo.get_active_categories(db, restaurant_id, skip=skip, limit=limit)
        items = [CategoryResponse.model_validate(c) for c in categories]
        
        pages = math.ceil(total / limit) if limit > 0 else 1
        page_num = (skip // limit) + 1 if limit > 0 else 1
        
        result = Page[CategoryResponse](
            items=items,
            total=total,
            page=page_num,
            size=limit,
            pages=pages
        )
        
        await cache.set(cache_key, result, ttl_seconds=300)
        return result

    async def get_category(self, db: AsyncSession, category_id: int, restaurant_id: int) -> CategoryResponse:
        cache_key = f"category_{category_id}:rest_{restaurant_id}"
        cached_result = await cache.get(cache_key)
        if cached_result:
            return cached_result

        category = await category_repo.get(db, id=category_id)
        if not category or category.restaurant_id != restaurant_id or not category.is_active:
            raise NotFoundException("Category not found")
            
        result = CategoryResponse.model_validate(category)
        await cache.set(cache_key, result, ttl_seconds=300)
        return result

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
    ) -> Page[ProductResponse]:
        cache_key = f"products:rest_{restaurant_id}:cat_{category_id}:avail_{available_only}:feat_{is_featured}:off_{is_offer}:search_{search_query}:sort_{sort_by}:skip_{skip}:limit_{limit}"
        cached_result = await cache.get(cache_key)
        if cached_result:
            return cached_result
            
        products, total = await product_repo.get_products(
            db, restaurant_id, category_id, available_only, is_featured, is_offer, search_query, sort_by, skip, limit
        )
        
        items = [ProductResponse.model_validate(p) for p in products]
        pages = math.ceil(total / limit) if limit > 0 else 1
        page_num = (skip // limit) + 1 if limit > 0 else 1
        
        result = Page[ProductResponse](
            items=items,
            total=total,
            page=page_num,
            size=limit,
            pages=pages
        )
        
        await cache.set(cache_key, result, ttl_seconds=300)
        return result

    async def get_product(self, db: AsyncSession, product_id: int, restaurant_id: int) -> ProductResponse:
        cache_key = f"product_{product_id}:rest_{restaurant_id}"
        cached_result = await cache.get(cache_key)
        if cached_result:
            return cached_result

        product = await product_repo.get_product_details(db, product_id, restaurant_id)
        if not product:
            raise NotFoundException("Product not found")
            
        result = ProductResponse.model_validate(product)
        await cache.set(cache_key, result, ttl_seconds=300)
        return result

    async def get_full_menu(self, db: AsyncSession, restaurant_id: int):
        from app.schemas.menu import MenuResponse
        cache_key = f"full_menu:rest_{restaurant_id}"
        cached_result = await cache.get(cache_key)
        if cached_result:
            return cached_result
            
        categories, _ = await category_repo.get_active_categories(db, restaurant_id, skip=0, limit=1000)
        products = await product_repo.get_all_menu_products(db, restaurant_id)
        
        result = MenuResponse(
            categories=[CategoryResponse.model_validate(c) for c in categories],
            products=[ProductResponse.model_validate(p) for p in products]
        )
        
        await cache.set(cache_key, result, ttl_seconds=600)
        return result

menu_service = MenuService()
