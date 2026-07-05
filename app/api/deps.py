from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database.session import get_db_session
from app.core.config import settings
from app.models.customer import Customer
from app.models.hub import RestaurantHubDevice
from app.core.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/verify-otp")

async def get_current_customer(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session)
) -> Customer:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        customer_id: str = payload.get("sub")
        if customer_id is None:
            raise UnauthorizedException("Could not validate credentials")
    except JWTError:
        raise UnauthorizedException("Could not validate credentials")
    
    stmt = select(Customer).filter(Customer.id == int(customer_id))
    result = await db.execute(stmt)
    customer = result.scalars().first()
    
    if customer is None:
        raise UnauthorizedException("Customer not found")
        
    return customer

async def get_hub_device(
    x_hub_api_key: str = Header(..., description="The API Key for the Restaurant Hub"),
    db: AsyncSession = Depends(get_db_session)
) -> RestaurantHubDevice:
    stmt = select(RestaurantHubDevice).filter(RestaurantHubDevice.api_key == x_hub_api_key).options(
        selectinload(RestaurantHubDevice.restaurant),
        selectinload(RestaurantHubDevice.branch)
    )
    result = await db.execute(stmt)
    device = result.scalars().first()
    
    if not device:
        raise UnauthorizedException("Invalid API Key")
        
    if device.status != "ACTIVE":
        raise UnauthorizedException("Device is disabled")
        
    if not device.restaurant.is_enabled:
        raise UnauthorizedException("Restaurant is inactive")
        
    if not device.branch.is_enabled:
        raise UnauthorizedException("Branch is inactive")
        
    return device
