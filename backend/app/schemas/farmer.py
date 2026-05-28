from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class FarmerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    car_number: Optional[str] = None


class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    car_number: Optional[str] = None


class FarmerResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    car_number: Optional[str] = None
    total_weight: Decimal
    total_amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
