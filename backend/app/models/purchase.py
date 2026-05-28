from sqlalchemy import Column, BigInteger, String, Numeric, Boolean, DateTime, ForeignKey, func
from app.models.base import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    farmer_id = Column(BigInteger, ForeignKey("farmers.id"))
    grain_type = Column(String(32), nullable=False)
    gross_weight = Column(Numeric(14, 2), nullable=False)
    empty_weight = Column(Numeric(14, 2))
    net_weight = Column(Numeric(14, 2))
    jin_weight = Column(Numeric(14, 2))
    unit_price = Column(Numeric(10, 4), nullable=False)
    total_amount = Column(Numeric(14, 2))
    status = Column(String(32), nullable=False, default="CREATED")
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
