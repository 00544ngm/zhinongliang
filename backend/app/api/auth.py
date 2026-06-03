from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["认证"])

MAX_LOGIN_FAILURES = 5
LOGIN_LOCK_MINUTES = 5
_login_failures: dict[str, tuple[int, datetime | None]] = {}


def _login_key(username: str) -> str:
    return username.strip().lower()


def _is_locked(username: str) -> bool:
    failures, locked_until = _login_failures.get(_login_key(username), (0, None))
    if not locked_until:
        return False
    if datetime.now() >= locked_until:
        _login_failures.pop(_login_key(username), None)
        return False
    return failures >= MAX_LOGIN_FAILURES


def _record_login_failure(username: str) -> None:
    key = _login_key(username)
    failures, _locked_until = _login_failures.get(key, (0, None))
    failures += 1
    locked_until = None
    if failures >= MAX_LOGIN_FAILURES:
        locked_until = datetime.now() + timedelta(minutes=LOGIN_LOCK_MINUTES)
    _login_failures[key] = (failures, locked_until)


def _clear_login_failures(username: str) -> None:
    _login_failures.pop(_login_key(username), None)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    if _is_locked(req.username):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="登录失败次数过多，请稍后再试")

    result = await db.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        _record_login_failure(req.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    _clear_login_failures(req.username)
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
