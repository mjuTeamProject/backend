from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from datetime import datetime, time

from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.ranking import RankingEntry, RankingPeriodEnum
from app.schemas.ranking import RankingListResponse, RankingRegisterRequest

router = APIRouter()

@router.get("/daily", response_model=RankingListResponse)
async def get_daily_ranking(db: AsyncSession = Depends(get_db)):
    today_start = datetime.combine(datetime.now().date(), time.min)

    query = select(RankingEntry).options(selectinload(RankingEntry.user)).where(
        RankingEntry.period == RankingPeriodEnum.DAILY,
        RankingEntry.period_start == today_start
    ).order_by(desc(RankingEntry.score)).limit(100)

    result = await db.execute(query)
    entries = result.scalars().all()

    response_list = []
    for entry in entries:
        response_list.append({
            "id": entry.id,
            "user_nickname": entry.user.nickname if entry.user else "알수없음",
            "user1_name": entry.user1_name,
            "user2_name": entry.user2_name,
            "period": entry.period,
            "score": entry.score,
            "rank": entry.rank,
            "intro_message": entry.intro_message,
            "period_start": entry.period_start,
            "period_end": entry.period_end,
            "created_at": entry.created_at
        })

    return {
        "period": RankingPeriodEnum.DAILY,
        "total_entries": len(response_list),
        "rankings": response_list
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_for_ranking(
        data: RankingRegisterRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    today_start = datetime.combine(datetime.now().date(), time.min)
    today_end = datetime.combine(datetime.now().date(), time.max)

    existing_query = select(RankingEntry).where(
        RankingEntry.user_id == current_user.id,
        RankingEntry.period == RankingPeriodEnum.DAILY,
        RankingEntry.period_start == today_start
    )
    existing_result = await db.execute(existing_query)
    existing_entry = existing_result.scalar_one_or_none()

    if existing_entry:
        existing_entry.score = data.score
        existing_entry.intro_message = data.intro_message
        existing_entry.user1_name = data.user1_name
        existing_entry.user2_name = data.user2_name
    else:
        new_entry = RankingEntry(
            user_id=current_user.id,
            period=RankingPeriodEnum.DAILY,
            score=data.score,
            intro_message=data.intro_message,
            user1_name=data.user1_name,
            user2_name=data.user2_name,
            period_start=today_start,
            period_end=today_end
        )
        db.add(new_entry)

    await db.commit()
    return {"message": "랭킹에 등록되었습니다!"}