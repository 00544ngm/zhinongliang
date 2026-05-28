from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.inventory import InventoryResponse
from app.schemas.common import ApiResponse
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/api/inventory", tags=["库存"])


@router.get("")
async def get_inventory(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InventoryService(db)
    inventory = await service.get_all()
    return ApiResponse(data=[InventoryResponse.model_validate(i) for i in inventory])
