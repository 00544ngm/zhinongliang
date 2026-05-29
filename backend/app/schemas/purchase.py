from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class PurchaseCreate(BaseModel):
    farmer_id: Optional[int] = None
    farmer_name: Optional[str] = None
    grain_type: str
    gross_weight: Decimal
    unit_price: Decimal


class PurchaseUpdateWeight(BaseModel):
    empty_weight: Decimal


class PurchaseComplete(BaseModel):
    pass


class PurchaseResponse(BaseModel):
    id: int
    farmer_id: Optional[int] = None
    farmer_name: Optional[str] = None
    grain_type: str
    gross_weight: Decimal
    empty_weight: Optional[Decimal] = None
    net_weight: Optional[Decimal] = None
    unit_price: Decimal
    total_amount: Optional[Decimal] = None
    status: str
    created_at: datetime
    updated_at: datetime
    empty_weighted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
