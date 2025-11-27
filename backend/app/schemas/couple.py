from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CoupleBase(BaseModel):
    couple_name: Optional[str] = None
    anniversary_date: Optional[datetime] = None


class CoupleCreate(BaseModel):
    partner_username: str = Field(..., description="Partner's username to connect with")
    couple_name: Optional[str] = None
    anniversary_date: Optional[datetime] = None


class CoupleUpdate(BaseModel):
    couple_name: Optional[str] = None
    anniversary_date: Optional[datetime] = None


class CoupleResponse(CoupleBase):
    id: int
    user1_id: int
    user2_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class PartnerConnectRequest(BaseModel):
    partner_username: str = Field(..., description="Username of partner to connect")


class PartnerDisconnectRequest(BaseModel):
    couple_id: int
