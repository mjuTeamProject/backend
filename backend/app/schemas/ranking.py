from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.ranking import RankingPeriodEnum

# 랭킹 등록 요청 (변화 없음)
class RankingRegisterRequest(BaseModel):
    score: float
    intro_message: str = Field(..., max_length=30)

# 랭킹 응답 (couple_id 삭제, user_nickname 추가)
class RankingEntryResponse(BaseModel):
    id: int
    user_nickname: str  # [변경] 랭킹 보여줄 때 닉네임이 필요함
    period: RankingPeriodEnum
    score: float
    rank: Optional[int] = None
    intro_message: Optional[str] = None
    period_start: datetime
    period_end: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class RankingListResponse(BaseModel):
    period: RankingPeriodEnum
    total_entries: int
    rankings: list[RankingEntryResponse]