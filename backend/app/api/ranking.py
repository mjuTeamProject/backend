from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/daily")
async def get_daily_ranking(
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get daily ranking leaderboard
    
    - **limit**: Maximum number of entries to return (default: 100)
    """
    # TODO: Implement ranking service
    return {"message": "Ranking service will be implemented"}


@router.get("/weekly")
async def get_weekly_ranking(
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get weekly ranking leaderboard
    """
    # TODO: Implement
    return {"message": "Weekly ranking"}


@router.post("/register")
async def register_for_ranking(
    intro_message: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Register current couple's score to ranking
    
    - **intro_message**: One-line introduction message (max 200 chars)
    """
    # TODO: Implement
    return {"message": "Register for ranking"}
