"""Initialize database with default admin user."""
import asyncio
from app.core.database import async_session
from app.models.base import Base
from app.core.database import engine
from app.core.security import hash_password
from app.models.user import User


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.username == "admin"))
        if not result.scalar_one_or_none():
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin",
            )
            session.add(admin)
            await session.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
