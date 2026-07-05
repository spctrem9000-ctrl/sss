from typing import List, Optional, Tuple
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.models.order import Order
from pydantic import BaseModel

class OrderRepository(BaseRepository[Order, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Order)

    async def get_order_details(self, db: AsyncSession, order_id: int, customer_id: Optional[int] = None) -> Optional[Order]:
        stmt = select(Order).filter(Order.id == order_id)
        if customer_id:
            stmt = stmt.filter(Order.customer_id == customer_id)
            
        stmt = stmt.options(
            selectinload(Order.items),
            selectinload(Order.history)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_customer_orders(
        self, 
        db: AsyncSession, 
        customer_id: int, 
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Order], int]:
        stmt = select(Order).filter(Order.customer_id == customer_id)
        
        if status:
            stmt = stmt.filter(Order.status == status)
            
        # Count total
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(count_stmt) or 0
        
        stmt = stmt.order_by(desc(Order.created_at)).offset(skip).limit(limit).options(
            selectinload(Order.items),
            selectinload(Order.history)
        )
        
        result = await db.execute(stmt)
        return list(result.scalars().all()), total

    async def get_branch_orders(
        self,
        db: AsyncSession,
        branch_id: int,
        status: Optional[str] = None
    ) -> List[Order]:
        stmt = select(Order).filter(Order.branch_id == branch_id)
        if status:
            stmt = stmt.filter(Order.status == status)
            
        stmt = stmt.order_by(Order.created_at).options(
            selectinload(Order.items),
            selectinload(Order.history)
        )
        
        result = await db.execute(stmt)
        return list(result.scalars().all())

order_repo = OrderRepository()
