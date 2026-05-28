from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, func
from app.models.base import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32))
    car_number = Column(String(32))
    total_weight = Column(Numeric(14, 2), default=0)
    total_amount = Column(Numeric(14, 2), default=0)
    deleted = Column(String(1), default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
