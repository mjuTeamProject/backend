from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.analysis import AnalysisStatusEnum


class DirectAnalysisRequest(BaseModel):
    """DB 조회 없이 직접 분석하기 위한 요청 스키마"""
    # 사용자 1 (본인)
    user1_name: Optional[str] = None
    user1_gender: int = Field(..., description="0=female, 1=male")
    user1_birth_year: int
    user1_birth_month: int
    user1_birth_day: int
    user1_birth_hour: int = 12  # 시간 모를 경우 기본값

    # 사용자 2 (상대방)
    user2_name: Optional[str] = None
    user2_gender: int = Field(..., description="0=female, 1=male")
    user2_birth_year: int
    user2_birth_month: int
    user2_birth_day: int
    user2_birth_hour: int = 12


class AnalysisRequestCreate(BaseModel):
    couple_id: int


class AnalysisRequestResponse(BaseModel):
    id: int
    couple_id: int
    status: AnalysisStatusEnum
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AnalysisResultResponse(BaseModel):
    id: int
    request_id: int
    compatibility_score: float
    detailed_scores: Optional[Dict[str, Any]] = None
    saju_data_user1: Optional[Dict[str, Any]] = None
    saju_data_user2: Optional[Dict[str, Any]] = None
    interpretation: Optional[str] = None
    certificate_image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True