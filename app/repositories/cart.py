from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.models.cart import Cart, CartItem
from pydantic import BaseModel

class CartRepository(BaseRepository[Cart, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Cart)

    async def get_active_cart(self, db: AsyncSession, customer_id: int, restaurant_id: int) -> Optional[Cart]:
        stmt = select(Cart).filter(
            Cart.customer_id == customer_id,
            Cart.restaurant_id == restaurant_id,
            Cart.status == "active"
        ).options(
            selectinload(Cart.items)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

class CartItemRepository(BaseRepository[CartItem, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(CartItem)
        
    async def get_cart_item(self, db: AsyncSession, cart_id: int, product_id: int, size_id: Optional[int] = None) -> Optional[CartItem]:
        stmt = select(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        )
        if size_id:
            stmt = stmt.filter(CartItem.size_id == size_id)
        else:
            stmt = stmt.filter(CartItem.size_id.is_(None))
            
        result = await db.execute(stmt)
        return result.scalars().first()

cart_repo = CartRepository()
cart_item_repo = CartItemRepository()
