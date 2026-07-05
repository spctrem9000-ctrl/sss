from typing import Any, Generic, List, Optional, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        return await self.repository.get(db, id)

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.repository.get_multi(db, skip=skip, limit=limit)

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        return await self.repository.create(db, obj_in=obj_in)

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: AsyncSession, id: Any) -> ModelType:
        return await self.repository.remove(db, id=id)
