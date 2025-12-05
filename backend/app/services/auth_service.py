from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import timedelta
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository, ProfileRepository
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserCreate
from app.utils.security import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token
from app.utils.validators import validate_username, validate_password, validate_nickname
from app.models.user import User, Profile


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.profile_repo = ProfileRepository(db)
    
    async def register(self, data: RegisterRequest) -> Token:
        valid, error = validate_username(data.username)
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        valid, error = validate_password(data.password)
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        valid, error = validate_nickname(data.nickname)
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        existing_user = await self.user_repo.get_by_username(data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if data.email:
            existing_email = await self.user_repo.get_by_email(data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        hashed_password = get_password_hash(data.password)
        user_data = UserCreate(
            username=data.username,
            email=data.email,
            nickname=data.nickname,
            password=data.password  # UserCreate requires password field
        )
        user = await self.user_repo.create(user_data, hashed_password)
        
        from app.schemas.user import ProfileCreate
        empty_profile = ProfileCreate()
        await self.profile_repo.create(user.id, empty_profile)
        
        await self.db.commit()
        
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return Token(access_token=access_token, refresh_token=refresh_token)
    
    async def login(self, data: LoginRequest) -> Token:
        user = await self.user_repo.get_by_username(data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return Token(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh_access_token(self, refresh_token: str) -> Token:
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )
        
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        new_access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return Token(access_token=new_access_token, refresh_token=new_refresh_token)
    
    async def get_current_user(self, token: str) -> User:
        payload = verify_token(token, token_type="access")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )
        
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user