from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.ranking import RankingPeriodEnum


class RankingEntryCreate(BaseModel):
    couple_id: int
    period: RankingPeriodEnum
    intro_message: Optional[str] = Field(None, max_length=200)


class RankingEntryResponse(BaseModel):
    id: int
    couple_id: int
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
