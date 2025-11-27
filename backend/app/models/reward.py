from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class BadgeTypeEnum(str, enum.Enum):
    TOP_10 = "top_10"
    TOP_50 = "top_50"
    TOP_100 = "top_100"
    PERFECT_MATCH = "perfect_match"  # 100점
    FIRST_ANALYSIS = "first_analysis"
    SHARE_MASTER = "share_master"  # 공유 10회 이상


class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    badge_type = Column(SQLEnum(BadgeTypeEnum), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")


class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")


class CouponTypeEnum(str, enum.Enum):
    CAFE_DISCOUNT = "cafe_discount"
    RESTAURANT_DISCOUNT = "restaurant_discount"
    MOVIE_DISCOUNT = "movie_discount"
    ACTIVITY_DISCOUNT = "activity_discount"


class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    coupon_type = Column(SQLEnum(CouponTypeEnum), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    discount_amount = Column(Integer, nullable=True)  # 할인 금액
    discount_percent = Column(Integer, nullable=True)  # 할인율
    partner_name = Column(String(100), nullable=True)  # 제휴사 이름
    code = Column(String(50), unique=True, nullable=False)  # 쿠폰 코드
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="coupons")


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    reward_type = Column(String(50), nullable=True)  # badge, coupon, points
    reward_id = Column(Integer, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
