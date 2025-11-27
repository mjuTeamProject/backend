"""
Compatibility Analysis Service
Handles compatibility analysis requests and results
"""
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime

from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.couple_repository import CoupleRepository
from app.repositories.user_repository import ProfileRepository
from app.models.analysis import AnalysisStatusEnum
from app.ai.saju_engine import get_engine


class AnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.analysis_repo = AnalysisRepository(db)
        self.couple_repo = CoupleRepository(db)
        self.profile_repo = ProfileRepository(db)
        self.engine = get_engine()
    
    async def create_analysis_for_couple(self, couple_id: int, user_id: int) -> dict:
        """
        Create compatibility analysis for a couple
        
        Requires both users to have complete birth information
        """
        # Get couple
        couple = await self.couple_repo.get_by_id(couple_id)
        if not couple:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Couple not found"
            )
        
        # Verify user is part of the couple
        if user_id not in [couple.user1_id, couple.user2_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not part of this couple"
            )
        
        # Get profiles
        profile1 = await self.profile_repo.get_by_user_id(couple.user1_id)
        profile2 = await self.profile_repo.get_by_user_id(couple.user2_id)
        
        if not profile1 or not profile2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both users must have profiles"
            )
        
        # Validate birth data
        if not all([
            profile1.birth_year, profile1.birth_month, profile1.birth_day, profile1.birth_hour,
            profile2.birth_year, profile2.birth_month, profile2.birth_day, profile2.birth_hour
        ]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both users must have complete birth information"
            )
        
        # Create analysis request
        request = await self.analysis_repo.create_request(couple_id)
        request.status = AnalysisStatusEnum.PROCESSING
        
        try:
            # Run AI analysis
            gender1 = 1 if profile1.gender == 'male' else 0
            gender2 = 1 if profile2.gender == 'male' else 0
            
            analysis_result = self.engine.analyze_compatibility(
                year1=profile1.birth_year,
                month1=profile1.birth_month,
                day1=profile1.birth_day,
                hour1=profile1.birth_hour,
                gender1=gender1,
                year2=profile2.birth_year,
                month2=profile2.birth_month,
                day2=profile2.birth_day,
                hour2=profile2.birth_hour,
                gender2=gender2
            )
            
            # Save result
            result = await self.analysis_repo.create_result(
                request_id=request.id,
                score=analysis_result['compatibility_score'],
                saju_data_user1=analysis_result['saju_data_user1'],
                saju_data_user2=analysis_result['saju_data_user2'],
                detailed_scores=analysis_result['detailed_scores'],
                interpretation=analysis_result['interpretation']
            )
            
            # Update request status
            request.status = AnalysisStatusEnum.COMPLETED
            request.completed_at = datetime.utcnow()
            
            await self.db.commit()
            
            return {
                'request_id': request.id,
                'result_id': result.id,
                'compatibility_score': result.compatibility_score,
                'interpretation': result.interpretation,
                'created_at': result.created_at
            }
            
        except Exception as e:
            request.status = AnalysisStatusEnum.FAILED
            await self.db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {str(e)}"
            )
    
    async def get_result_by_id(self, result_id: int, user_id: int) -> dict:
        """Get analysis result by ID"""
        result = await self.analysis_repo.get_result_by_id(result_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis result not found"
            )
        
        # Get request and verify access
        request = await self.analysis_repo.get_request_by_id(result.request_id)
        couple = await self.couple_repo.get_by_id(request.couple_id)
        
        if user_id not in [couple.user1_id, couple.user2_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return {
            'id': result.id,
            'request_id': result.request_id,
            'compatibility_score': result.compatibility_score,
            'saju_data_user1': result.saju_data_user1,
            'saju_data_user2': result.saju_data_user2,
            'detailed_scores': result.detailed_scores,
            'interpretation': result.interpretation,
            'certificate_image_url': result.certificate_image_url,
            'created_at': result.created_at
        }
    
    async def get_couple_history(self, couple_id: int, user_id: int) -> list:
        """Get all analysis history for a couple"""
        couple = await self.couple_repo.get_by_id(couple_id)
        if not couple:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Couple not found"
            )
        
        if user_id not in [couple.user1_id, couple.user2_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        requests = await self.analysis_repo.get_requests_by_couple(couple_id)
        
        history = []
        for req in requests:
            result = await self.analysis_repo.get_result_by_request_id(req.id)
            history.append({
                'request_id': req.id,
                'status': req.status,
                'created_at': req.created_at,
                'completed_at': req.completed_at,
                'result': {
                    'id': result.id,
                    'compatibility_score': result.compatibility_score,
                    'interpretation': result.interpretation
                } if result else None
            })
        
        return history
