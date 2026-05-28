from sqlalchemy import Column, BigInteger, String, Numeric
from app.models.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    grain_type = Column(String(32), unique=True, nullable=False)
    total_weight = Column(Numeric(14, 2), nullable=False, default=0)
