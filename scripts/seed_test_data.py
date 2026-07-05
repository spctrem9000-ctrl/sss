import asyncio
import sys
import os

# Add the parent directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import async_session_maker
from app.models.restaurant import Restaurant
from app.models.branch import Branch
from app.models.customer import Customer
from app.models.hub import RestaurantHubDevice
import uuid

async def seed_data():
    async with async_session_maker() as db:
        try:
            # 1. Create a Test Restaurant
            restaurant = Restaurant(name="Test Restaurant", currency="USD", country="USA")
            db.add(restaurant)
            await db.flush()

            # 2. Create a Test Branch
            branch = Branch(restaurant_id=restaurant.id, name="Main Branch", is_default=True)
            db.add(branch)
            await db.flush()

            # 3. Create a Test Customer
            customer = Customer(
                phone_number="+1234567890",
                first_name="Test",
                last_name="User",
                is_active=True
            )
            db.add(customer)
            await db.flush()

            # 4. Create a Hub Device
            api_key = "HUB-SECRET-KEY-123"
            hub = RestaurantHubDevice(
                restaurant_id=restaurant.id,
                branch_id=branch.id,
                device_name="Kitchen Display 1",
                device_uuid=str(uuid.uuid4()),
                api_key=api_key,
                status="ACTIVE"
            )
            db.add(hub)

            await db.commit()

            print("========================================")
            print("✅ Test Data Generated Successfully!")
            print("========================================")
            print(f"Restaurant ID: {restaurant.id}")
            print(f"Branch ID:     {branch.id}")
            print(f"Customer ID:   {customer.id}")
            print(f"Hub API Key:   {api_key}")
            print("========================================")
            
        except Exception as e:
            await db.rollback()
            print(f"Error seeding data: {e}")

if __name__ == "__main__":
    asyncio.run(seed_data())
