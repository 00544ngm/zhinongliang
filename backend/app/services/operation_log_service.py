from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.operation_log_repository import OperationLogRepository
from app.models.operation_log import OperationLog
from typing import Any


class OperationLogService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = OperationLogRepository(db)

    async def log(self, user_id: int, operation_type: str, target_type: str,
                  target_id: int, old_data: dict[str, Any] | None = None,
                  new_data: dict[str, Any] | None = None):
        log_entry = OperationLog(
            user_id=user_id,
            operation_type=operation_type,
            target_type=target_type,
            target_id=target_id,
            old_data=old_data,
            new_data=new_data,
        )
        await self.repo.add(log_entry)

    async def get_recent(self, limit: int = 50) -> list[OperationLog]:
        return await self.repo.list(limit=limit)
