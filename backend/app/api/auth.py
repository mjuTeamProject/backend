from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, Token, RefreshTokenRequest
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.register(data)


@router.post("/login", response_model=Token)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.login(data)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(data.refresh_token)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    auth_service = AuthService(db)
    return await auth_service.get_current_user(token)