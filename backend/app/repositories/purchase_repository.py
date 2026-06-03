from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.repositories.base import BaseRepository
from app.models.purchase import Purchase
from datetime import date, datetime, time, timedelta


class PurchaseRepository(BaseRepository[Purchase]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Purchase)

    async def get_by_status(self, status: str, offset: int = 0, limit: int = 200) -> list[Purchase]:
        from sqlalchemy import select
        result = await self.db.execute(
            select(Purchase).where(Purchase.status == status, Purchase.deleted == False)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_today(self, offset: int = 0, limit: int = 200) -> list[Purchase]:
        start = datetime.combine(date.today(), time.min)
        end = start + timedelta(days=1)
        result = await self.db.execute(
            select(Purchase)
            .where(
                Purchase.created_at >= start,
                Purchase.created_at < end,
                Purchase.deleted == False,
            )
            .order_by(Purchase.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_date_range(self, start: date, end: date, offset: int = 0, limit: int = 200) -> list[Purchase]:
        start_dt = datetime.combine(start, time.min)
        end_dt = datetime.combine(end + timedelta(days=1), time.min)
        result = await self.db.execute(
            select(Purchase)
            .where(
                Purchase.created_at >= start_dt,
                Purchase.created_at < end_dt,
                Purchase.deleted == False,
            )
            .order_by(Purchase.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_farmer_id(self, farmer_id: int, offset: int = 0, limit: int = 200) -> list[Purchase]:
        result = await self.db.execute(
            select(Purchase)
            .where(
                Purchase.farmer_id == farmer_id,
                Purchase.deleted == False,
            )
            .order_by(Purchase.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
