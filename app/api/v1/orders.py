from typing import List, Optional
from fastapi import APIRouter, Depends, Header, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.api.deps import get_current_customer
from app.models.customer import Customer
from app.schemas.order import CheckoutRequest, OrderResponse, OrderDetailResponse
from app.services.checkout import checkout_service
from app.services.order import order_service
from app.repositories.order import order_repo

router = APIRouter()

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Order Checkout"
)
async def submit_order(
    request: CheckoutRequest,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await checkout_service.process_checkout(db, current_customer.id, x_restaurant_id, request)

@router.get(
    "/history",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Order History"
)
async def get_order_history(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    orders, total = await order_repo.get_customer_orders(db, current_customer.id, status, skip, limit)
    return [OrderResponse.model_validate(o) for o in orders]

@router.get(
    "/{order_id}",
    response_model=OrderDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Order Details"
)
async def get_order_details(
    order_id: int,
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await order_service.get_order_details(db, current_customer.id, order_id)

@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancel Order"
)
async def cancel_order(
    order_id: int,
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await order_service.cancel_order(db, current_customer.id, order_id)
