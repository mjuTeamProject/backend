from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class RankingPeriodEnum(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"


class RankingEntry(Base):
    __tablename__ = "ranking_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    couple_id = Column(Integer, ForeignKey("couples.id", ondelete="CASCADE"), nullable=False)
    period = Column(SQLEnum(RankingPeriodEnum), nullable=False)
    score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=True)
    intro_message = Column(String(200), nullable=True)  # 한 줄 소개
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint: one entry per couple per period
    __table_args__ = (
        UniqueConstraint('couple_id', 'period', 'period_start', name='uix_couple_period'),
    )
    
    # Relationships
    couple = relationship("Couple", back_populates="ranking_entries")
