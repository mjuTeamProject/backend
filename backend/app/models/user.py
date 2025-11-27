from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    couple = relationship("Couple", foreign_keys="Couple.user1_id", back_populates="user1")
    couple_as_partner = relationship("Couple", foreign_keys="Couple.user2_id", back_populates="user2")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    coupons = relationship("Coupon", back_populates="user", cascade="all, delete-orphan")
    share_logs = relationship("ShareLog", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    birth_year = Column(Integer, nullable=True)
    birth_month = Column(Integer, nullable=True)
    birth_day = Column(Integer, nullable=True)
    birth_hour = Column(Integer, nullable=True)
    gender = Column(SQLEnum(GenderEnum), nullable=True)
    zodiac_sign = Column(String(20), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")
