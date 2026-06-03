from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.repositories.base import BaseRepository
from app.models.inventory import Inventory
from decimal import Decimal


class InventoryRepository(BaseRepository[Inventory]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Inventory)

    async def get_by_grain_type(self, grain_type: str) -> Inventory | None:
        result = await self.db.execute(
            select(Inventory).where(Inventory.grain_type == grain_type)
        )
        return result.scalar_one_or_none()

    async def add_weight(self, grain_type: str, weight: Decimal):
        existing = await self.get_by_grain_type(grain_type)
        if existing:
            await self.db.execute(
                update(Inventory)
                .where(Inventory.grain_type == grain_type)
                .values(total_weight=Inventory.total_weight + weight)
            )
        else:
            inv = Inventory(grain_type=grain_type, total_weight=weight)
            self.db.add(inv)
        await self.db.flush()

    async def subtract_weight(self, grain_type: str, weight: Decimal):
        existing = await self.get_by_grain_type(grain_type)
        if existing:
            new_weight = existing.total_weight - weight
            if new_weight < 0:
                new_weight = Decimal("0")
            await self.db.execute(
                update(Inventory)
                .where(Inventory.grain_type == grain_type)
                .values(total_weight=new_weight)
            )
            await self.db.flush()
