from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.analysis import DirectAnalysisRequest
from app.ai.saju_engine import get_engine

router = APIRouter()


@router.post("/calculate")
async def calculate_compatibility(
        data: DirectAnalysisRequest,
):
    try:
        engine = get_engine()

        result = engine.analyze_compatibility(
            year1=data.user1_birth_year,
            month1=data.user1_birth_month,
            day1=data.user1_birth_day,
            hour1=data.user1_birth_hour,
            gender1=data.user1_gender,

            year2=data.user2_birth_year,
            month2=data.user2_birth_month,
            day2=data.user2_birth_day,
            hour2=data.user2_birth_hour,
            gender2=data.user2_gender
        )

        result['user1_name'] = data.user1_name
        result['user2_name'] = data.user2_name

        return result

    except Exception as e:
        print(f"Analysis Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/{result_id}")
async def get_analysis_result(
        result_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    from app.services.analysis_service import AnalysisService
    analysis_service = AnalysisService(db)
    return await analysis_service.get_result_by_id(result_id, current_user.id)


@router.get("/couple/{couple_id}/history")
async def get_analysis_history(
        couple_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    from app.services.analysis_service import AnalysisService
    analysis_service = AnalysisService(db)
    return await analysis_service.get_couple_history(couple_id, current_user.id)
