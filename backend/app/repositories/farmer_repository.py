from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.farmer import Farmer


class FarmerRepository(BaseRepository[Farmer]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Farmer)

    async def search_by_name(self, keyword: str) -> list[Farmer]:
        result = await self.db.execute(
            select(Farmer).where(
                Farmer.deleted == "0",
                Farmer.name.ilike(f"%{keyword}%"),
            )
        )
        return list(result.scalars().all())
