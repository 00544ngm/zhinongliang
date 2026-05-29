from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from typing import Optional


class InventoryResponse(BaseModel):
    id: int
    grain_type: str
    total_weight: Decimal

    class Config:
        from_attributes = True


class DailyRecord(BaseModel):
    date: date
    total_weight: Decimal
    last_purchase_at: Optional[datetime] = None


class GrainDailyResponse(BaseModel):
    grain_type: str
    total_weight: Decimal
    daily: list[DailyRecord]


class InventoryDailyResponse(BaseModel):
    grain_types: list[GrainDailyResponse]
    page: int
    page_size: int
    total_pages: int
