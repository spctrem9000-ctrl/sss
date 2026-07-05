from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.repositories.base import BaseRepository
from app.models.application import Application
from pydantic import BaseModel

class ApplicationRepository(BaseRepository[Application, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Application)

    async def get_by_app_key(self, db: AsyncSession, app_key: str) -> Optional[Application]:
        stmt = (
            select(Application)
            .options(joinedload(Application.restaurant).joinedload(Application.restaurant.class_.branches))
            .filter(Application.app_key == app_key)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

application_repo = ApplicationRepository()
