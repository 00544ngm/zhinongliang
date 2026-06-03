from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = InventoryRepository(db)

    async def add_stock(self, grain_type: str, weight: Decimal):
        if weight is None:
            return
        await self.repo.add_weight(grain_type, weight)

    async def remove_stock(self, grain_type: str, weight: Decimal):
        if weight is None:
            return
        await self.repo.subtract_weight(grain_type, weight)

    async def get_all(self) -> list:
        return await self.repo.list()

    async def get_by_grain_type(self, grain_type: str):
        return await self.repo.get_by_grain_type(grain_type)
