from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.services.analysis_service import AnalysisService
from app.repositories.couple_repository import CoupleRepository

router = APIRouter()


@router.post("/calculate")
async def calculate_compatibility(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate compatibility score for current user and their partner
    
    Requires both users to have complete birth information in their profiles.
    Returns the analysis result with compatibility score and interpretation.
    """
    # Get user's couple
    couple_repo = CoupleRepository(db)
    couple = await couple_repo.get_by_user_id(current_user.id)
    
    if not couple:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have a partner connection. Please connect with a partner first."
        )
    
    # Run analysis
    analysis_service = AnalysisService(db)
    return await analysis_service.create_analysis_for_couple(couple.id, current_user.id)


@router.get("/{result_id}")
async def get_analysis_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get analysis result by result ID
    
    Returns detailed compatibility analysis including:
    - Compatibility score
    - Saju data for both users
    - Detailed trait analysis
    - AI interpretation
    """
    analysis_service = AnalysisService(db)
    return await analysis_service.get_result_by_id(result_id, current_user.id)


@router.get("/couple/{couple_id}/history")
async def get_analysis_history(
    couple_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all analysis history for a couple
    
    Returns a list of all compatibility analyses performed for this couple.
    """
    analysis_service = AnalysisService(db)
    return await analysis_service.get_couple_history(couple_id, current_user.id)
