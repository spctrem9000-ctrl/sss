from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.api.deps import get_hub_device
from app.models.hub import RestaurantHubDevice
from app.schemas.hub import HeartbeatRequest, OrderStatusUpdateRequest, HubSettingsResponse, HubDeviceResponse
from app.schemas.order import OrderDetailResponse
from app.schemas.menu import MenuResponse
from app.services.hub import hub_service

router = APIRouter()

@router.post("/heartbeat", status_code=status.HTTP_200_OK, summary="Send Heartbeat")
async def heartbeat(
    request: HeartbeatRequest,
    device: RestaurantHubDevice = Depends(get_hub_device),
    db: AsyncSession = Depends(get_db_session)
):
    return await hub_service.process_heartbeat(db, device, request.version, request.device_name)

@router.get("/orders/new", response_model=List[OrderDetailResponse], status_code=status.HTTP_200_OK, summary="Get New Orders")
async def get_new_orders(
    device: RestaurantHubDevice = Depends(get_hub_device),
    db: AsyncSession = Depends(get_db_session)
):
    return await hub_service.get_new_orders(db, device)

@router.post("/orders/{order_id}/download", status_code=status.HTTP_200_OK, summary="Acknowledge Order Download")
async def acknowledge_order(
    order_id: int,
    device: RestaurantHubDevice = Depends(get_hub_device),
    db: AsyncSession = Depends(get_db_session)
):
    return await hub_service.acknowledge_order(db, device, order_id)

@router.patch("/orders/{order_id}/status", status_code=status.HTTP_200_OK, summary="Update Order Status")
async def update_order_status(
    order_id: int,
    request: OrderStatusUpdateRequest,
    device: RestaurantHubDevice = Depends(get_hub_device),
    db: AsyncSession = Depends(get_db_session)
):
    return await hub_service.update_order_status(db, device, order_id, request.status)

@router.get("/products", response_model=MenuResponse, status_code=status.HTTP_200_OK, summary="Get Products")
async def get_products(
    device: RestaurantHubDevice = Depends(get_hub_device),
    db: AsyncSession = Depends(get_db_session)
):
    return await hub_service.get_products(db, device)

@router.get("/settings", response_model=HubSettingsResponse, status_code=status.HTTP_200_OK, summary="Get Settings")
async def get_settings(
    device: RestaurantHubDevice = Depends(get_hub_device),
    db: AsyncSession = Depends(get_db_session)
):
    return await hub_service.get_settings(db, device)

@router.get("/device", response_model=HubDeviceResponse, status_code=status.HTTP_200_OK, summary="Get Device Info")
async def get_device(
    device: RestaurantHubDevice = Depends(get_hub_device)
):
    return HubDeviceResponse.model_validate(device)
