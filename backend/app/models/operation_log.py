from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, JSON
from app.models.base import Base


class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    operation_type = Column(String(64))
    target_type = Column(String(64))
    target_id = Column(BigInteger)
    old_data = Column(JSON)
    new_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
