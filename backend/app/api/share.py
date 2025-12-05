from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/log")
async def log_share(
    analysis_id: int,
    platform: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return {"message": "Share logged"}


@router.get("/image/{analysis_id}")
async def generate_certificate_image(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return {"message": "Image generation service will be implemented"}