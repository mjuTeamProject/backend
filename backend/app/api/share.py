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
    """
    Log SNS share activity
    
    - **analysis_id**: ID of the analysis result being shared
    - **platform**: Platform name (kakao, instagram, facebook, twitter, download)
    """
    # TODO: Implement share service
    return {"message": "Share logged"}


@router.get("/image/{analysis_id}")
async def generate_certificate_image(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate and return certificate image for analysis result
    """
    # TODO: Implement image generation
    return {"message": "Image generation service will be implemented"}
