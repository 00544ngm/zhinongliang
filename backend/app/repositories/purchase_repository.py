from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.repositories.base import BaseRepository
from app.models.purchase import Purchase
from datetime import date


class PurchaseRepository(BaseRepository[Purchase]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Purchase)

    async def get_by_status(self, status: str) -> list[Purchase]:
        from sqlalchemy import select
        result = await self.db.execute(
            select(Purchase).where(Purchase.status == status, Purchase.deleted == False)
        )
        return list(result.scalars().all())

    async def get_today(self) -> list[Purchase]:
        result = await self.db.execute(
            select(Purchase)
            .where(
                func.date(Purchase.created_at) == date.today(),
                Purchase.deleted == False,
            )
            .order_by(Purchase.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_date_range(self, start: date, end: date) -> list[Purchase]:
        result = await self.db.execute(
            select(Purchase)
            .where(
                func.date(Purchase.created_at).between(start, end),
                Purchase.deleted == False,
            )
            .order_by(Purchase.created_at.desc())
        )
        return list(result.scalars().all())
