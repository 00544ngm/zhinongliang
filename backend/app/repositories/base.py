from typing import Any, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    def __init__(self, db: AsyncSession, model: type[ModelT]):
        self.db = db
        self.model = model

    async def get_by_id(self, id: int) -> ModelT | None:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(self.model))
        return result.scalar()

    async def add(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def delete(self, obj: ModelT):
        await self.db.delete(obj)
        await self.db.flush()
