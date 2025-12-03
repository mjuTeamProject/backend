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
        # 로그인 여부와 상관없이 분석 가능하도록 user dependency를 제거하거나 optional로 처리할 수 있습니다.
        # 현재는 순수 계산 로직만 수행하므로 DB 세션도 필요 없습니다.
):
    """
    [직접 분석 API]
    DB에 저장된 커플 정보를 조회하지 않고,
    요청 Body로 전달받은 두 사람의 생년월일 정보를 바탕으로 즉시 궁합을 분석합니다.
    """
    try:
        engine = get_engine()

        # AI 사주 분석 엔진 호출
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

        # 이름 정보는 결과에 포함시켜 줌 (프론트 표시용)
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
    """
    Get analysis result by result ID
    (기존에 저장된 결과를 조회하는 경우에만 사용)
    """
    from app.services.analysis_service import AnalysisService
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
    """
    from app.services.analysis_service import AnalysisService
    analysis_service = AnalysisService(db)
    return await analysis_service.get_couple_history(couple_id, current_user.id)