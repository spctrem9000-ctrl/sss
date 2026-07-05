from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import OrderStatusHistory
from app.repositories.order import order_repo
from app.schemas.order import OrderDetailResponse, OrderResponse
from app.core.exceptions import BadRequestException, NotFoundException

class OrderService:
    async def get_order_details(self, db: AsyncSession, customer_id: int, order_id: int) -> OrderDetailResponse:
        order = await order_repo.get_order_details(db, order_id, customer_id=customer_id)
        if not order:
            raise NotFoundException("Order not found")
        return OrderDetailResponse.model_validate(order)

    async def cancel_order(self, db: AsyncSession, customer_id: int, order_id: int) -> OrderResponse:
        order = await order_repo.get_order_details(db, order_id, customer_id=customer_id)
        if not order:
            raise NotFoundException("Order not found")
            
        if order.status != "NEW":
            raise BadRequestException(f"Cannot cancel order in status: {order.status}")
            
        order.status = "CANCELLED"
        
        history = OrderStatusHistory(
            order_id=order.id,
            old_status="NEW",
            new_status="CANCELLED",
            created_by=customer_id
        )
        db.add(history)
        
        await db.commit()
        await db.refresh(order)
        return OrderResponse.model_validate(order)

order_service = OrderService()
