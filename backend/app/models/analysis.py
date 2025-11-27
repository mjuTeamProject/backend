from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AnalysisStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRequest(Base):
    __tablename__ = "analysis_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    couple_id = Column(Integer, ForeignKey("couples.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(AnalysisStatusEnum), default=AnalysisStatusEnum.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    couple = relationship("Couple", back_populates="analysis_requests")
    result = relationship("AnalysisResult", back_populates="request", uselist=False, cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("analysis_requests.id", ondelete="CASCADE"), unique=True, nullable=False)
    compatibility_score = Column(Float, nullable=False)  # 궁합 점수 (0-100)
    detailed_scores = Column(JSON, nullable=True)  # 세부 점수 (sal0, sal1 등)
    saju_data_user1 = Column(JSON, nullable=True)  # 사용자1 사주 데이터
    saju_data_user2 = Column(JSON, nullable=True)  # 사용자2 사주 데이터
    interpretation = Column(Text, nullable=True)  # AI 해석 텍스트
    certificate_image_url = Column(String(255), nullable=True)  # 인증서 이미지 URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    request = relationship("AnalysisRequest", back_populates="result")
