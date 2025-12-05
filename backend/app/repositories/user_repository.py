from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User, Profile
from app.schemas.user import UserCreate, ProfileCreate, ProfileUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            nickname=user_data.nickname
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update(self, user: User) -> User:
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.flush()


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        result = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def create(self, user_id: int, profile_data: ProfileCreate) -> Profile:
        profile = Profile(
            user_id=user_id,
            **profile_data.model_dump(exclude_unset=True)
        )
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile
    
    async def update(self, profile: Profile, profile_data: ProfileUpdate) -> Profile:
        for field, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
        
        await self.db.flush()
        await self.db.refresh(profile)
        return profile