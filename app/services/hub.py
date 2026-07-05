from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.hub import RestaurantHubDevice
from app.models.order import OrderStatusHistory
from app.repositories.order import order_repo
from app.schemas.order import OrderDetailResponse
from app.schemas.hub import HubSettingsResponse
from app.schemas.menu import MenuResponse
from app.services.menu import menu_service
from app.core.exceptions import BadRequestException, NotFoundException
from loguru import logger

class HubService:
    async def process_heartbeat(self, db: AsyncSession, device: RestaurantHubDevice, version: str, device_name: str) -> dict:
        device.last_seen = datetime.now(timezone.utc)
        device.version = version
        device.device_name = device_name
        await db.commit()
        logger.info(f"Hub Heartbeat: {device.device_name} ({device.device_uuid})")
        return {"status": "ok"}
        
    async def get_settings(self, db: AsyncSession, device: RestaurantHubDevice) -> HubSettingsResponse:
        return HubSettingsResponse(
            restaurant_settings=device.restaurant.settings or {},
            branch_settings=device.branch.settings or {}
        )
        
    async def get_products(self, db: AsyncSession, device: RestaurantHubDevice) -> MenuResponse:
        # Re-use the all-in-one menu endpoint logic for the Hub
        return await menu_service.get_full_menu(db, device.restaurant_id)
        
    async def get_new_orders(self, db: AsyncSession, device: RestaurantHubDevice) -> List[OrderDetailResponse]:
        orders = await order_repo.get_branch_orders(db, device.branch_id, status="NEW")
        return [OrderDetailResponse.model_validate(o) for o in orders]
        
    async def acknowledge_order(self, db: AsyncSession, device: RestaurantHubDevice, order_id: int) -> dict:
        order = await order_repo.get_order_details(db, order_id)
        if not order or order.branch_id != device.branch_id:
            raise NotFoundException("Order not found for this branch")
            
        if order.status != "NEW":
            raise BadRequestException(f"Order is already in status: {order.status}")
            
        order.status = "DOWNLOADED"
        history = OrderStatusHistory(
            order_id=order.id,
            old_status="NEW",
            new_status="DOWNLOADED",
            created_by=device.id # Can represent the hub device
        )
        db.add(history)
        await db.commit()
        logger.info(f"Hub {device.device_name} downloaded Order {order.order_number}")
        return {"status": "success"}

    async def update_order_status(self, db: AsyncSession, device: RestaurantHubDevice, order_id: int, new_status: str) -> dict:
        allowed_statuses = ["ACCEPTED", "PREPARING", "READY", "OUT_FOR_DELIVERY", "DELIVERED", "REJECTED", "CANCELLED"]
        if new_status not in allowed_statuses:
            raise BadRequestException("Invalid status")
            
        order = await order_repo.get_order_details(db, order_id)
        if not order or order.branch_id != device.branch_id:
            raise NotFoundException("Order not found for this branch")
            
        old_status = order.status
        order.status = new_status
        history = OrderStatusHistory(
            order_id=order.id,
            old_status=old_status,
            new_status=new_status,
            created_by=device.id
        )
        db.add(history)
        await db.commit()
        logger.info(f"Order {order.order_number} status updated to {new_status} by Hub {device.device_name}")
        return {"status": "success"}

hub_service = HubService()
