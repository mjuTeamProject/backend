from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository, ProfileRepository
from app.repositories.couple_repository import CoupleRepository
from app.schemas.user import UserUpdate, UserWithProfile, ProfileUpdate
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.profile_repo = ProfileRepository(db)
        self.couple_repo = CoupleRepository(db)
    
    async def get_user_with_profile(self, user_id: int) -> UserWithProfile:
        """Get user with profile"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Explicitly load profile to avoid lazy loading issues
        profile = await self.profile_repo.get_by_user_id(user_id)
        
        # Convert to dict and build response
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nickname": user.nickname,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "profile": {
                "id": profile.id,
                "user_id": profile.user_id,
                "birth_year": profile.birth_year,
                "birth_month": profile.birth_month,
                "birth_day": profile.birth_day,
                "birth_hour": profile.birth_hour,
                "gender": profile.gender,
                "zodiac_sign": profile.zodiac_sign,
                "avatar_url": profile.avatar_url,
                "created_at": profile.created_at
            } if profile else None
        }
        
        return UserWithProfile.model_validate(user_dict)
    
    async def update_user(self, user_id: int, data: UserUpdate) -> UserWithProfile:
        """Update user information"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        if data.nickname is not None:
            user.nickname = data.nickname
        if data.email is not None:
            # Check if email is already taken by another user
            existing = await self.user_repo.get_by_email(data.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            user.email = data.email
        
        await self.user_repo.update(user)
        await self.db.commit()
        
        return await self.get_user_with_profile(user_id)
    
    async def update_profile(self, user_id: int, data: ProfileUpdate) -> UserWithProfile:
        """Update user profile"""
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        await self.profile_repo.update(profile, data)
        await self.db.commit()
        
        return await self.get_user_with_profile(user_id)
    
    async def get_partner(self, user_id: int) -> Optional[UserWithProfile]:
        """Get user's partner"""
        couple = await self.couple_repo.get_by_user_id(user_id)
        if not couple:
            return None
        
        # Determine partner ID
        partner_id = couple.user2_id if couple.user1_id == user_id else couple.user1_id
        
        return await self.get_user_with_profile(partner_id)
    
    async def connect_partner(self, user_id: int, partner_username: str) -> dict:
        """Connect with a partner"""
        # Get partner by username
        partner = await self.user_repo.get_by_username(partner_username)
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner not found"
            )
        
        # Check if trying to connect with self
        if partner.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot connect with yourself"
            )
        
        # Check if user already has a partner
        existing_couple = await self.couple_repo.get_by_user_id(user_id)
        if existing_couple:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a partner connection"
            )
        
        # Check if partner already has a connection
        partner_couple = await self.couple_repo.get_by_user_id(partner.id)
        if partner_couple:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Partner already has a connection"
            )
        
        # Create couple
        couple = await self.couple_repo.create(user_id, partner.id)
        await self.db.commit()
        
        # Get partner with profile
        partner_with_profile = await self.get_user_with_profile(partner.id)
        
        return {
            "message": "Successfully connected with partner",
            "couple_id": couple.id,
            "partner": partner_with_profile
        }
    
    async def disconnect_partner(self, user_id: int) -> dict:
        """Disconnect from partner"""
        couple = await self.couple_repo.get_by_user_id(user_id)
        if not couple:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No partner connection found"
            )
        
        await self.couple_repo.delete(couple)
        await self.db.commit()
        
        return {"message": "Successfully disconnected from partner"}
