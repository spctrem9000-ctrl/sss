from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.api.deps import get_current_customer
from app.models.customer import Customer
from app.schemas.cart import (
    CartItemAddRequest, 
    CartItemUpdateQuantityRequest, 
    ApplyCouponRequest, 
    CartResponse
)
from app.services.cart import cart_service

router = APIRouter()

@router.get(
    "",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Active Cart"
)
async def get_cart(
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.get_cart(db, current_customer.id, x_restaurant_id)

@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Add Item to Cart"
)
async def add_item(
    request: CartItemAddRequest,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    x_branch_id: int = Header(..., description="The ID of the branch"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.add_item(db, current_customer.id, x_restaurant_id, x_branch_id, request)

@router.patch(
    "/items/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Item Quantity"
)
async def update_item_quantity(
    item_id: int,
    request: CartItemUpdateQuantityRequest,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.update_item_quantity(db, current_customer.id, x_restaurant_id, item_id, request.quantity)

@router.delete(
    "/items/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove Item from Cart"
)
async def remove_item(
    item_id: int,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.remove_item(db, current_customer.id, x_restaurant_id, item_id)

@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    summary="Clear Cart"
)
async def clear_cart(
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.clear_cart(db, current_customer.id, x_restaurant_id)

@router.post(
    "/calculate",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate Cart Totals"
)
async def calculate_cart(
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.calculate_cart(db, current_customer.id, x_restaurant_id)

@router.post(
    "/apply-coupon",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Apply Coupon to Cart"
)
async def apply_coupon(
    request: ApplyCouponRequest,
    x_restaurant_id: int = Header(..., description="The ID of the restaurant (Tenant)"),
    current_customer: Customer = Depends(get_current_customer),
    db: AsyncSession = Depends(get_db_session)
):
    return await cart_service.apply_coupon(db, current_customer.id, x_restaurant_id, request.code)
