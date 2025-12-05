from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.ranking import RankingPeriodEnum

class RankingRegisterRequest(BaseModel):
    score: float
    intro_message: str = Field(..., max_length=30)
    user1_name: str
    user2_name: str

class RankingEntryResponse(BaseModel):
    id: int
    user_nickname: str
    user1_name: str
    user2_name: str
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