from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.farmer_repository import FarmerRepository
from app.repositories.operation_log_repository import OperationLogRepository
from app.models.purchase import Purchase
from app.models.farmer import Farmer
from app.services.inventory_service import InventoryService
from app.services.farmer_service import FarmerService
from app.services.operation_log_service import OperationLogService
from datetime import date


class PurchaseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.purchase_repo = PurchaseRepository(db)
        self.inventory_service = InventoryService(db)
        self.farmer_service = FarmerService(db)
        self.log_service = OperationLogService(db)

    async def create(self, grain_type: str, gross_weight: Decimal, unit_price: Decimal,
                     farmer_id: int | None = None, farmer_name: str | None = None,
                     user_id: int = 0) -> Purchase:
        if farmer_id is None and farmer_name:
            farmer = await self.farmer_service.get_or_create(farmer_name)
            farmer_id = farmer.id

        purchase = Purchase(
            farmer_id=farmer_id,
            grain_type=grain_type,
            gross_weight=gross_weight,
            unit_price=unit_price,
            status="GROSS_WEIGHTED",
        )
        purchase = await self.purchase_repo.add(purchase)

        await self.log_service.log(
            user_id=user_id,
            operation_type="CREATE_PURCHASE",
            target_type="Purchase",
            target_id=purchase.id,
            new_data={
                "grain_type": grain_type,
                "gross_weight": str(gross_weight),
                "unit_price": str(unit_price),
            },
        )
        return purchase

    async def set_empty_weight(self, purchase_id: int, empty_weight: Decimal,
                               user_id: int = 0) -> Purchase:
        purchase = await self.purchase_repo.get_by_id(purchase_id)
        if not purchase or purchase.deleted:
            raise ValueError("收购单不存在")

        old_status = purchase.status
        net_weight = purchase.gross_weight - empty_weight
        jin_weight = net_weight * Decimal("2")
        total_amount = jin_weight * purchase.unit_price

        purchase.empty_weight = empty_weight
        purchase.net_weight = net_weight
        purchase.jin_weight = jin_weight
        purchase.total_amount = total_amount
        purchase.status = "EMPTY_WEIGHTED"

        await self.db.flush()

        await self.log_service.log(
            user_id=user_id,
            operation_type="SET_EMPTY_WEIGHT",
            target_type="Purchase",
            target_id=purchase.id,
            old_data={"status": old_status},
            new_data={
                "status": "EMPTY_WEIGHTED",
                "empty_weight": str(empty_weight),
                "net_weight": str(net_weight),
                "total_amount": str(total_amount),
            },
        )
        return purchase

    async def complete(self, purchase_id: int, user_id: int = 0) -> Purchase:
        purchase = await self.purchase_repo.get_by_id(purchase_id)
        if not purchase or purchase.deleted:
            raise ValueError("收购单不存在")
        if purchase.status != "EMPTY_WEIGHTED":
            raise ValueError("收购单状态不正确，需要先称空车")

        old_status = purchase.status
        purchase.status = "COMPLETED"
        await self.db.flush()

        await self.inventory_service.add_stock(
            grain_type=purchase.grain_type,
            weight=purchase.net_weight,
        )

        if purchase.farmer_id:
            await self.farmer_service.update_stats(
                farmer_id=purchase.farmer_id,
                weight=purchase.net_weight,
                amount=purchase.total_amount,
            )

        await self.log_service.log(
            user_id=user_id,
            operation_type="COMPLETE_PURCHASE",
            target_type="Purchase",
            target_id=purchase.id,
            old_data={"status": old_status},
            new_data={"status": "COMPLETED"},
        )
        return purchase

    async def get_today(self) -> list[Purchase]:
        return await self.purchase_repo.get_today()

    async def get_by_date_range(self, start: date, end: date) -> list[Purchase]:
        return await self.purchase_repo.get_by_date_range(start, end)

    async def get_by_id(self, purchase_id: int) -> Purchase | None:
        return await self.purchase_repo.get_by_id(purchase_id)

    async def get_pending(self) -> list[Purchase]:
        return await self.purchase_repo.get_by_status("GROSS_WEIGHTED")
