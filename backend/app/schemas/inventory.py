from pydantic import BaseModel
from decimal import Decimal


class InventoryResponse(BaseModel):
    id: int
    grain_type: str
    total_weight: Decimal

    class Config:
        from_attributes = True
