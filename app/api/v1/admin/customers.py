from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database.session import get_db_session
from app.models.admin import AdminUser
from app.models.customer import Customer
from app.models.checkout import LoyaltyAccount
from app.api.deps import get_current_admin
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter()

class CustomerLoyaltyResponse(BaseModel):
    id: int
    phone_number: str
    name: str | None
    is_active: bool
    points_balance: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[CustomerLoyaltyResponse])
async def get_customers(
    admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_session)
):
    # For now, we return all customers. In a real scenario, loyalty points are per-restaurant.
    # We will join Customer and LoyaltyAccount.
    stmt = select(Customer, LoyaltyAccount).outerjoin(
        LoyaltyAccount, Customer.id == LoyaltyAccount.customer_id
    )
    result = await db.execute(stmt)
    
    customers_data = []
    for customer, loyalty in result.all():
        customers_data.append({
            "id": customer.id,
            "phone_number": customer.phone_number,
            "name": customer.name,
            "is_active": customer.is_active,
            "points_balance": loyalty.points_balance if loyalty else 0,
            "created_at": customer.created_at
        })
        
    return customers_data
