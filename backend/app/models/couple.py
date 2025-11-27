from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Couple(Base):
    __tablename__ = "couples"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    couple_name = Column(String(100), nullable=True)  # 커플 닉네임
    anniversary_date = Column(DateTime(timezone=True), nullable=True)  # 기념일
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id], back_populates="couple")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="couple_as_partner")
    analysis_requests = relationship("AnalysisRequest", back_populates="couple", cascade="all, delete-orphan")
    ranking_entries = relationship("RankingEntry", back_populates="couple", cascade="all, delete-orphan")
