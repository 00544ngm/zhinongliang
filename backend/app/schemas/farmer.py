from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class FarmerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    id_card: Optional[str] = None


class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None


class FarmerResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    id_card: Optional[str] = None
    total_gross_weight: Optional[Decimal] = Decimal("0")
    total_empty_weight: Optional[Decimal] = Decimal("0")
    total_weight: Optional[Decimal] = Decimal("0")
    total_amount: Optional[Decimal] = Decimal("0")
    created_at: datetime

    class Config:
        from_attributes = True
