from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.user import GenderEnum


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    email: Optional[EmailStr] = None
    nickname: str = Field(..., min_length=2, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Profile Schemas
class ProfileBase(BaseModel):
    birth_year: Optional[int] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None
    birth_hour: Optional[int] = None
    gender: Optional[GenderEnum] = None
    zodiac_sign: Optional[str] = None
    avatar_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Complete User with Profile
class UserWithProfile(UserResponse):
    profile: Optional[ProfileResponse] = None
    
    class Config:
        from_attributes = True
