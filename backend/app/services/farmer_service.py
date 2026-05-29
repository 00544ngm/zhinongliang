from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.repositories.farmer_repository import FarmerRepository
from app.models.farmer import Farmer


class FarmerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = FarmerRepository(db)

    async def get_or_create(self, name: str) -> Farmer:
        results = await self.repo.search_by_name(name)
        if results:
            return results[0]
        farmer = Farmer(name=name)
        return await self.repo.add(farmer)

    async def update_stats(self, farmer_id: int, gross_weight: Decimal, empty_weight: Decimal, net_weight: Decimal, amount: Decimal):
        await self.db.execute(
            update(Farmer)
            .where(Farmer.id == farmer_id)
            .values(
                total_gross_weight=Farmer.total_gross_weight + gross_weight,
                total_empty_weight=Farmer.total_empty_weight + empty_weight,
                total_weight=Farmer.total_weight + net_weight,
                total_amount=Farmer.total_amount + amount,
            )
        )
        await self.db.flush()

    async def get_all(self) -> list[Farmer]:
        return await self.repo.list()

    async def search(self, keyword: str) -> list[Farmer]:
        return await self.repo.search_by_name(keyword)

    async def get_by_id(self, farmer_id: int) -> Farmer | None:
        return await self.repo.get_by_id(farmer_id)

    async def update(self, farmer_id: int, name: str | None = None,
                     phone: str | None = None, id_card: str | None = None) -> Farmer:
        farmer = await self.repo.get_by_id(farmer_id)
        if not farmer:
            raise ValueError("农户不存在")
        if name:
            farmer.name = name
        if phone is not None:
            farmer.phone = phone
        if id_card is not None:
            farmer.id_card = id_card
        await self.db.flush()
        return farmer
