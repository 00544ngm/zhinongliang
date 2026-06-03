from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Numeric, Boolean, DateTime, ForeignKey, Index
from app.models.base import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    farmer_id = Column(BigInteger, ForeignKey("farmers.id"))
    grain_type = Column(String(32), nullable=False)
    gross_weight = Column(Numeric(14, 2), nullable=False)
    empty_weight = Column(Numeric(14, 2))
    net_weight = Column(Numeric(14, 2))
    unit_price = Column(Numeric(10, 4), nullable=False)
    total_amount = Column(Numeric(14, 2))
    status = Column(String(32), nullable=False, default="CREATED")
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    empty_weighted_at = Column(DateTime)
    completed_at = Column(DateTime)


Index("idx_purchases_created_deleted", Purchase.created_at, Purchase.deleted)
Index("idx_purchases_status_deleted", Purchase.status, Purchase.deleted)
Index("idx_purchases_farmer_deleted", Purchase.farmer_id, Purchase.deleted)
