from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models.analysis import AnalysisRequest, AnalysisResult, AnalysisStatusEnum


class AnalysisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_request(self, couple_id: int) -> AnalysisRequest:
        request = AnalysisRequest(
            couple_id=couple_id,
            status=AnalysisStatusEnum.PENDING
        )
        self.db.add(request)
        await self.db.flush()
        await self.db.refresh(request)
        return request
    
    async def get_request_by_id(self, request_id: int) -> Optional[AnalysisRequest]:
        result = await self.db.execute(
            select(AnalysisRequest).where(AnalysisRequest.id == request_id)
        )
        return result.scalar_one_or_none()
    
    async def get_requests_by_couple(self, couple_id: int) -> List[AnalysisRequest]:
        result = await self.db.execute(
            select(AnalysisRequest)
            .where(AnalysisRequest.couple_id == couple_id)
            .order_by(AnalysisRequest.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def create_result(self, request_id: int, score: float, **kwargs) -> AnalysisResult:
        result = AnalysisResult(
            request_id=request_id,
            compatibility_score=score,
            **kwargs
        )
        self.db.add(result)
        await self.db.flush()
        await self.db.refresh(result)
        return result
    
    async def get_result_by_id(self, result_id: int) -> Optional[AnalysisResult]:
        result = await self.db.execute(
            select(AnalysisResult).where(AnalysisResult.id == result_id)
        )
        return result.scalar_one_or_none()
    
    async def get_result_by_request_id(self, request_id: int) -> Optional[AnalysisResult]:
        result = await self.db.execute(
            select(AnalysisResult).where(AnalysisResult.request_id == request_id)
        )
        return result.scalar_one_or_none()