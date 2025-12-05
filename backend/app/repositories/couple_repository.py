from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional
from app.models.couple import Couple


class CoupleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, couple_id: int) -> Optional[Couple]:
        result = await self.db.execute(select(Couple).where(Couple.id == couple_id))
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> Optional[Couple]:
        result = await self.db.execute(
            select(Couple).where(
                or_(
                    Couple.user1_id == user_id,
                    Couple.user2_id == user_id
                ),
                Couple.is_active == True
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_users(self, user1_id: int, user2_id: int) -> Optional[Couple]:
        result = await self.db.execute(
            select(Couple).where(
                or_(
                    (Couple.user1_id == user1_id) & (Couple.user2_id == user2_id),
                    (Couple.user1_id == user2_id) & (Couple.user2_id == user1_id)
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def create(self, user1_id: int, user2_id: int, **kwargs) -> Couple:
        couple = Couple(
            user1_id=user1_id,
            user2_id=user2_id,
            **kwargs
        )
        self.db.add(couple)
        await self.db.flush()
        await self.db.refresh(couple)
        return couple
    
    async def update(self, couple: Couple) -> Couple:
        await self.db.flush()
        await self.db.refresh(couple)
        return couple
    
    async def delete(self, couple: Couple):
        couple.is_active = False
        await self.db.flush()