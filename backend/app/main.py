from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api import auth, purchases, inventory, farmers, dashboard, background_photos
from app.models.base import Base
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="智农粮 - 家庭粮食收购站工业级数字化管理系统",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PHOTO_DIR = PROJECT_ROOT / "frontend" / "public" / "photos"
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/photos", StaticFiles(directory=PHOTO_DIR), name="photos")

app.include_router(auth.router)
app.include_router(purchases.router)
app.include_router(inventory.router)
app.include_router(farmers.router)
app.include_router(dashboard.router)
app.include_router(background_photos.router)
