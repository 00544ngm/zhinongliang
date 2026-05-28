from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.operation_log import OperationLog


class OperationLogRepository(BaseRepository[OperationLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, OperationLog)
