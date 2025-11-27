from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.analysis import AnalysisStatusEnum


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


class CompatibilityAnalysisRequest(BaseModel):
    """Request for compatibility analysis with birth data"""
    user1_birth_year: int = Field(..., ge=1900, le=2025)
    user1_birth_month: int = Field(..., ge=1, le=12)
    user1_birth_day: int = Field(..., ge=1, le=31)
    user1_birth_hour: int = Field(..., ge=0, le=23)
    user1_gender: int = Field(..., ge=0, le=1, description="0=female, 1=male")
    
    user2_birth_year: int = Field(..., ge=1900, le=2025)
    user2_birth_month: int = Field(..., ge=1, le=12)
    user2_birth_day: int = Field(..., ge=1, le=31)
    user2_birth_hour: int = Field(..., ge=0, le=23)
    user2_gender: int = Field(..., ge=0, le=1, description="0=female, 1=male")
