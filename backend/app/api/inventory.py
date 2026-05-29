from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.purchase import Purchase
from app.schemas.inventory import InventoryResponse, InventoryDailyResponse, GrainDailyResponse, DailyRecord
from app.schemas.common import ApiResponse
from app.services.inventory_service import InventoryService
from math import ceil

router = APIRouter(prefix="/api/inventory", tags=["库存"])


@router.get("")
async def get_inventory(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InventoryService(db)
    inventory = await service.get_all()
    return ApiResponse(data=[InventoryResponse.model_validate(i) for i in inventory])


@router.get("/daily")
async def get_daily_inventory(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get all grain types with total weight
    service = InventoryService(db)
    inventory_list = await service.get_all()
    total_map = {i.grain_type: i.total_weight for i in inventory_list}

    # Get distinct grain types that have completed purchases
    result = await db.execute(
        select(Purchase.grain_type).where(
            Purchase.deleted == False,
            Purchase.status == "COMPLETED",
        ).distinct()
    )
    grain_types = [row[0] for row in result.all()]

    # Include grain types from inventory that may not have completed purchases yet
    all_types = set(grain_types) | set(total_map.keys())
    all_types.discard("其他")

    grain_daily_list = []
    for gt in sorted(all_types):
        # Count total daily records for this grain type
        count_result = await db.execute(
            select(func.count(func.distinct(
                cast(Purchase.created_at, Date)
            ))).where(
                Purchase.grain_type == gt,
                Purchase.deleted == False,
                Purchase.status == "COMPLETED",
            )
        )
        total_days = count_result.scalar() or 0
        total_pages = max(1, ceil(total_days / page_size))

        if page > total_pages:
            daily_records = []
        else:
            # Get daily aggregate for this grain type
            offset = (page - 1) * page_size
            daily_result = await db.execute(
                select(
                    cast(Purchase.created_at, Date).label("purchase_date"),
                    func.sum(Purchase.net_weight).label("day_weight"),
                    func.max(Purchase.updated_at).label("last_time"),
                ).where(
                    Purchase.grain_type == gt,
                    Purchase.deleted == False,
                    Purchase.status == "COMPLETED",
                )
                .group_by(cast(Purchase.created_at, Date))
                .order_by(cast(Purchase.created_at, Date).desc())
                .offset(offset)
                .limit(page_size)
            )
            daily_records = [
                DailyRecord(
                    date=row.purchase_date,
                    total_weight=row.day_weight or 0,
                    last_purchase_at=row.last_time,
                )
                for row in daily_result.all()
            ]

        grain_daily_list.append(GrainDailyResponse(
            grain_type=gt,
            total_weight=total_map.get(gt, 0),
            daily=daily_records,
        ))

    max_pages = 1
    for g in grain_daily_list:
        count_result = await db.execute(
            select(func.count(func.distinct(
                cast(Purchase.created_at, Date)
            ))).where(
                Purchase.grain_type == g.grain_type,
                Purchase.deleted == False,
                Purchase.status == "COMPLETED",
            )
        )
        total_days = count_result.scalar() or 0
        g_total_pages = max(1, ceil(total_days / page_size))
        if g_total_pages > max_pages:
            max_pages = g_total_pages

    return ApiResponse(data=InventoryDailyResponse(
        grain_types=grain_daily_list,
        page=page,
        page_size=page_size,
        total_pages=max_pages,
    ))
