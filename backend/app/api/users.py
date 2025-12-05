from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserWithProfile, UserUpdate, ProfileUpdate
from app.services.user_service import UserService
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserWithProfile)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.get_user_with_profile(current_user.id)


@router.put("/me", response_model=UserWithProfile)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.update_user(current_user.id, data)


@router.put("/me/profile", response_model=UserWithProfile)
async def update_my_detailed_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.update_profile(current_user.id, data)


@router.get("/me/partner", response_model=UserWithProfile)
async def get_my_partner(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    partner = await user_service.get_partner(current_user.id)
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No partner connection found"
        )
    return partner