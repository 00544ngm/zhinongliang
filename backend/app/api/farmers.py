from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.farmer import FarmerCreate, FarmerUpdate, FarmerResponse
from app.schemas.common import ApiResponse
from app.services.farmer_service import FarmerService

router = APIRouter(prefix="/api/farmers", tags=["农户"])


@router.get("")
async def list_farmers(
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmerService(db)
    if keyword:
        farmers = await service.search(keyword)
    else:
        farmers = await service.get_all()
    return ApiResponse(data=[FarmerResponse.model_validate(f) for f in farmers])


@router.post("")
async def create_farmer(
    req: FarmerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmerService(db)
    farmer = await service.get_or_create(req.name)
    if req.phone or req.car_number:
        farmer = await service.update(
            farmer_id=farmer.id,
            phone=req.phone,
            car_number=req.car_number,
        )
    return ApiResponse(data=FarmerResponse.model_validate(farmer))


@router.get("/{farmer_id}")
async def get_farmer(
    farmer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmerService(db)
    farmer = await service.get_by_id(farmer_id)
    if not farmer or farmer.deleted == "1":
        raise HTTPException(status_code=404, detail="农户不存在")
    return ApiResponse(data=FarmerResponse.model_validate(farmer))


@router.put("/{farmer_id}")
async def update_farmer(
    farmer_id: int,
    req: FarmerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FarmerService(db)
    try:
        farmer = await service.update(
            farmer_id=farmer_id,
            name=req.name,
            phone=req.phone,
            car_number=req.car_number,
        )
        return ApiResponse(data=FarmerResponse.model_validate(farmer))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
