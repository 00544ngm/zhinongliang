from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, Index, text
from app.models.base import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32))
    id_card = Column(String(18))
    total_gross_weight = Column(Numeric(14, 2), default=0, server_default=text("0"))
    total_empty_weight = Column(Numeric(14, 2), default=0, server_default=text("0"))
    total_weight = Column(Numeric(14, 2), default=0)
    total_amount = Column(Numeric(14, 2), default=0)
    deleted = Column(String(1), default="0")
    created_at = Column(DateTime, default=datetime.now)


Index("idx_farmers_name_deleted", Farmer.name, Farmer.deleted)
