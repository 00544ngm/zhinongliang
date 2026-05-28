from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.purchase import Purchase
from app.models.farmer import Farmer
from app.schemas.common import ApiResponse
from datetime import date

router = APIRouter(prefix="/api/dashboard", tags=["仪表盘"])


@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today_purchases = await db.execute(
        select(func.count(), func.coalesce(func.sum(Purchase.total_amount), 0))
        .where(func.date(Purchase.created_at) == date.today(), Purchase.deleted == False)
    )
    count, amount = today_purchases.one()

    farmer_count = await db.execute(select(func.count()).select_from(Farmer).where(Farmer.deleted == "0"))
    total_farmers = farmer_count.scalar()

    return ApiResponse(data={
        "today_purchases": count,
        "today_amount": str(amount),
        "total_farmers": total_farmers,
    })
