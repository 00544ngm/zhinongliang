from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.farmer import Farmer
from app.models.user import User
from app.schemas.purchase import PurchaseCreate, PurchaseUpdateWeight, PurchaseResponse
from app.schemas.common import ApiResponse
from app.services.purchase_service import PurchaseService
from app.services.farmer_service import FarmerService
from datetime import date

router = APIRouter(prefix="/api/purchases", tags=["收购单"])


async def _purchase_to_response(purchase, db) -> dict:
    data = {
        "id": purchase.id,
        "farmer_id": purchase.farmer_id,
        "farmer_name": None,
        "grain_type": purchase.grain_type,
        "gross_weight": purchase.gross_weight,
        "empty_weight": purchase.empty_weight,
        "net_weight": purchase.net_weight,
        "unit_price": purchase.unit_price,
        "total_amount": purchase.total_amount,
        "status": purchase.status,
        "created_at": purchase.created_at,
        "updated_at": purchase.updated_at,
        "empty_weighted_at": purchase.empty_weighted_at,
        "completed_at": purchase.completed_at,
    }
    if purchase.farmer_id:
        farmer = await FarmerService(db).get_by_id(purchase.farmer_id)
        if farmer:
            data["farmer_name"] = farmer.name
    return data


async def _purchases_to_response(purchases, db) -> list[dict]:
    farmer_ids = {p.farmer_id for p in purchases if p.farmer_id}
    farmer_names: dict[int, str] = {}
    if farmer_ids:
        result = await db.execute(select(Farmer.id, Farmer.name).where(Farmer.id.in_(farmer_ids)))
        farmer_names = {farmer_id: name for farmer_id, name in result.all()}

    result = []
    for purchase in purchases:
        data = {
            "id": purchase.id,
            "farmer_id": purchase.farmer_id,
            "farmer_name": farmer_names.get(purchase.farmer_id),
            "grain_type": purchase.grain_type,
            "gross_weight": purchase.gross_weight,
            "empty_weight": purchase.empty_weight,
            "net_weight": purchase.net_weight,
            "unit_price": purchase.unit_price,
            "total_amount": purchase.total_amount,
            "status": purchase.status,
            "created_at": purchase.created_at,
            "updated_at": purchase.updated_at,
            "empty_weighted_at": purchase.empty_weighted_at,
            "completed_at": purchase.completed_at,
        }
        result.append(data)
    return result


@router.post("")
async def create_purchase(
    req: PurchaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchase = await service.create(
        grain_type=req.grain_type,
        gross_weight=req.gross_weight,
        unit_price=req.unit_price,
        farmer_id=req.farmer_id,
        farmer_name=req.farmer_name,
        user_id=current_user.id,
    )
    data = await _purchase_to_response(purchase, db)
    return ApiResponse(data=data)


@router.post("/{purchase_id}/set-empty-weight")
async def set_empty_weight(
    purchase_id: int,
    req: PurchaseUpdateWeight,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    try:
        purchase = await service.set_empty_weight(
            purchase_id=purchase_id,
            empty_weight=req.empty_weight,
            user_id=current_user.id,
        )
        data = await _purchase_to_response(purchase, db)
        return ApiResponse(data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{purchase_id}/complete")
async def complete_purchase(
    purchase_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    try:
        purchase = await service.complete(
            purchase_id=purchase_id,
            user_id=current_user.id,
        )
        data = await _purchase_to_response(purchase, db)
        return ApiResponse(data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/today")
async def get_today(
    offset: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchases = await service.get_today(offset=offset, limit=min(limit, 500))
    result = await _purchases_to_response(purchases, db)
    return ApiResponse(data=result)


@router.get("/pending")
async def get_pending(
    offset: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchases = await service.get_pending(offset=offset, limit=min(limit, 500))
    result = await _purchases_to_response(purchases, db)
    return ApiResponse(data=result)


@router.get("/range")
async def get_by_date_range(
    start: date,
    end: date,
    offset: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchases = await service.get_by_date_range(start, end, offset=offset, limit=min(limit, 500))
    result = await _purchases_to_response(purchases, db)
    return ApiResponse(data=result)


@router.get("/by-farmer/{farmer_id}")
async def get_purchases_by_farmer(
    farmer_id: int,
    offset: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchases = await service.get_by_farmer_id(farmer_id, offset=offset, limit=min(limit, 500))
    result = await _purchases_to_response(purchases, db)
    return ApiResponse(data=result)


@router.get("/{purchase_id}")
async def get_purchase(
    purchase_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PurchaseService(db)
    purchase = await service.get_by_id(purchase_id)
    if not purchase or purchase.deleted:
        raise HTTPException(status_code=404, detail="收购单不存在")
    data = await _purchase_to_response(purchase, db)
    return ApiResponse(data=data)
