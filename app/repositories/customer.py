from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.customer import Customer
from pydantic import BaseModel

class CustomerCreate(BaseModel):
    phone_number: str

class CustomerRepository(BaseRepository[Customer, CustomerCreate, BaseModel]):
    def __init__(self):
        super().__init__(Customer)

    async def get_by_phone(self, db: AsyncSession, phone_number: str) -> Optional[Customer]:
        result = await db.execute(select(Customer).filter(Customer.phone_number == phone_number))
        return result.scalars().first()

customer_repo = CustomerRepository()
