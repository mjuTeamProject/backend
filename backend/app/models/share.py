from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class SharePlatformEnum(str, enum.Enum):
    KAKAO = "kakao"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    DOWNLOAD = "download"  # 이미지 다운로드


class ShareLog(Base):
    __tablename__ = "share_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    analysis_result_id = Column(Integer, ForeignKey("analysis_results.id", ondelete="SET NULL"), nullable=True)
    platform = Column(SQLEnum(SharePlatformEnum), nullable=False)
    shared_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="share_logs")
