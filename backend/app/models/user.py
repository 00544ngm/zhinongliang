from sqlalchemy import Column, BigInteger, String, DateTime, func
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default="operator")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
