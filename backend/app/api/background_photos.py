from pathlib import Path

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/background-photos", tags=["background-photos"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PHOTO_DIR = PROJECT_ROOT / "frontend" / "public" / "photos" / "backgrounds"
PHOTO_URL_PREFIX = "/photos/backgrounds"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@router.get("")
async def list_background_photos(
    current_user: User = Depends(get_current_user),
):
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)

    photos = []
    for file_path in sorted(PHOTO_DIR.iterdir(), key=lambda item: item.name.lower()):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        photos.append(
            {
                "name": file_path.stem,
                "filename": file_path.name,
                "url": f"{PHOTO_URL_PREFIX}/{file_path.name}",
            }
        )

    return {"data": photos}
