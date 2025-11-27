from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.couple import PartnerConnectRequest, CoupleResponse
from app.services.user_service import UserService
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/connect", status_code=status.HTTP_201_CREATED)
async def connect_with_partner(
    data: PartnerConnectRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Connect with a partner
    
    - **partner_username**: Username of the partner to connect with
    
    Both users must not have existing partner connections.
    """
    user_service = UserService(db)
    return await user_service.connect_partner(current_user.id, data.partner_username)


@router.delete("/disconnect")
async def disconnect_from_partner(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Disconnect from current partner
    
    This will deactivate the couple relationship.
    """
    user_service = UserService(db)
    return await user_service.disconnect_partner(current_user.id)
