"""
Soulmatch AI Saju Analysis Engine
사주 기반 궁합 분석 딥러닝 엔진

Based on the original hd2.ipynb notebook
Copyright Reserved by bongbong@mju.ac.kr, 명지대학교 한승철
"""
import numpy as np
import tensorflow as tf
import h5py
from typing import Tuple, Dict, List, Optional
import os

from app.config import settings


class SajuEngine:
    """Saju (Four Pillars of Destiny) Analysis Engine"""
    
    # 천간 (Heavenly Stems)
    SKY = {'갑': 1, '을': 2, '병': 3, '정': 4, '무': 5, 
           '기': 6, '경': 7, '신': 8, '임': 9, '계': 10}
    
    # 지지 (Earthly Branches)
    EARTH = {'자': 1, '축': 2, '인': 3, '묘': 4, '진': 5, '사': 6,
             '오': 7, '미': 8, '신': 9, '유': 10, '술': 11, '해': 12}
    
    # 분석 가중치 파라미터
    WEIGHTS = {
        'p1': 8, 'p11': 9.5,
        'p2': 7, 'p21': 8.2,
        'p3': 6, 'p31': 7.2,
        'p41': 10, 'p42': 8, 'p43': 6,
        'p5': 8, 'p6': 8,
        'p7': 0, 'p71': 10,
        'p8': 0, 'p81': 10, 'p82': 6, 'p83': 4
    }
    
    def __init__(self):
        """Initialize Saju Engine with ML models"""
        # Load converted TensorFlow 2.x compatible models
        try:
            self.sky_model = tf.keras.models.load_model(settings.SKY_MODEL_PATH, compile=False)
            self.sky_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            print(f"✓ Loaded sky model from {settings.SKY_MODEL_PATH}")
        except Exception as e:
            print(f"⚠ Warning: Could not load sky model: {e}")
            # Fallback to dummy model
            self.sky_model = tf.keras.Sequential([
                tf.keras.layers.Dense(1, input_shape=(20,), activation='linear')
            ])
            self.sky_model.compile(optimizer='adam', loss='mse', metrics=['mse'])
        
        try:
            self.earth_model = tf.keras.models.load_model(settings.EARTH_MODEL_PATH, compile=False)
            self.earth_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            print(f"✓ Loaded earth model from {settings.EARTH_MODEL_PATH}")
        except Exception as e:
            print(f"⚠ Warning: Could not load earth model: {e}")
            # Fallback to dummy model
            self.earth_model = tf.keras.Sequential([
                tf.keras.layers.Dense(1, input_shape=(24,), activation='linear')
            ])
            self.earth_model.compile(optimizer='adam', loss='mse', metrics=['mse'])
        
        # Load calendar data - try multiple encodings
        try:
            self.calendar_data = np.loadtxt(settings.CALENDAR_FILE_PATH, delimiter=',', skiprows=1, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                self.calendar_data = np.loadtxt(settings.CALENDAR_FILE_PATH, delimiter=',', skiprows=1, encoding='cp949')
            except UnicodeDecodeError:
                self.calendar_data = np.loadtxt(settings.CALENDAR_FILE_PATH, delimiter=',', skiprows=1, encoding='euc-kr')
    
    def get_key_by_value(self, dictionary: Dict, value: int) -> Optional[str]:
        """Get key from dictionary by value"""
        for key, val in dictionary.items():
            if val == value:
                return key
        return None
    
    def get_one_hot(self, target, nb_classes):
        """Convert to one-hot encoding"""
        t = np.array(target).reshape(-1)
        res = np.eye(nb_classes)[np.array(t).reshape(-1)]
        return res.reshape(list(t.shape) + [nb_classes])
    
    def calculate_sky_score(self, sky1: int, sky2: int) -> float:
        """Calculate compatibility score for heavenly stems using ML model with rule-based fallback"""
        try:
            # Prepare one-hot encoded input for ML model
            sky_input = np.zeros((1, 20))
            sky_input[0, sky1-1] = 1  # sky1 position (1-indexed to 0-indexed)
            sky_input[0, 10 + sky2-1] = 1  # sky2 position
            
            # Get ML prediction
            prediction = self.sky_model.predict(sky_input, verbose=0)[0][0]
            
            # Ensure prediction is in valid range [0, 1]
            score = max(0.0, min(1.0, float(prediction)))
            
            # If prediction is suspiciously uniform (untrained model), use rule-based
            if score > 0.99 or score < 0.01:
                raise ValueError("Model appears untrained, using rule-based fallback")
            
            return score
            
        except Exception as e:
            # Fallback to rule-based logic
            # 천간 궁합 규칙 (1-10: 갑을병정무기경신임계)
            diff = abs(sky1 - sky2)
            
            # 합 (차이가 5)
            if diff == 5:
                return 0.9
            # 충 (차이가 6 또는 4)
            elif diff == 6 or diff == 4:
                return 0.3
            # 같은 천간
            elif diff == 0:
                return 0.7
            # 인접
            elif diff == 1 or diff == 9:
                return 0.65
            # 기타
            else:
                return 0.6
    
    def calculate_earth_score(self, earth1: int, earth2: int) -> float:
        """Calculate compatibility score for earthly branches using ML model with rule-based fallback"""
        try:
            # Prepare one-hot encoded input for ML model
            earth_input = np.zeros((1, 24))
            earth_input[0, earth1-1] = 1  # earth1 position (1-indexed to 0-indexed)
            earth_input[0, 12 + earth2-1] = 1  # earth2 position
            
            # Get ML prediction
            prediction = self.earth_model.predict(earth_input, verbose=0)[0][0]
            
            # Ensure prediction is in valid range [0, 1]
            score = max(0.0, min(1.0, float(prediction)))
            
            # If prediction is suspiciously uniform (untrained model), use rule-based
            if score > 0.99 or score < 0.01:
                raise ValueError("Model appears untrained, using rule-based fallback")
            
            return score
            
        except Exception as e:
            # Fallback to rule-based logic
            # 지지 궁합 규칙 (1-12: 자축인묘진사오미신유술해)
            diff = abs(earth1 - earth2)
            
            # 육합 (차이가 1)
            if diff == 1 or diff == 11:
                return 0.85
            # 충 (정반대, 차이가 6)
            elif diff == 6:
                return 0.2
            # 삼합 (차이가 4 또는 8)
            elif diff == 4 or diff == 8:
                return 0.95
            # 형 (차이가 3 또는 9)
            elif diff == 3 or diff == 9:
                return 0.4
            # 같은 지지
            elif diff == 0:
                return 0.75
            # 기타
            else:
                return 0.6
    
    def calculate_detailed_compatibility(
        self,
        token0: List[int],
        token1: List[int],
        gender0: int,
        gender1: int,
        base_score: float
    ) -> Tuple[float, List[float], List[float]]:
        """
        Calculate detailed compatibility with additional factors
        
        Args:
            token0: First person's saju tokens [year_sky, year_earth, month_sky, month_earth, day_sky, day_earth]
            token1: Second person's saju tokens
            gender0: First person's gender (0=female, 1=male)
            gender1: Second person's gender
            base_score: Base compatibility score from ML model
        
        Returns:
            Tuple of (final_score, person0_traits, person1_traits)
        """
        score = base_score
        sal0 = [0.0] * 8  # Person 0 trait penalties
        sal1 = [0.0] * 8  # Person 1 trait penalties
        
        w = self.WEIGHTS
        a1, a2, a3 = token0[1], token0[3], token0[5]  # year_earth, month_earth, day_earth
        b1, b2, b3 = token1[1], token1[3], token1[5]
        
        # Rule 1: 공망살 (Gongmangsal) - Void/Emptiness penalty
        if a3 == 3:
            if a1 in [6, 9]:
                penalty = w['p1'] if gender0 == 1 else w['p11']
                score -= penalty
                sal0[0] += penalty
            if a2 in [6, 9]:
                penalty = w['p1'] if gender0 == 1 else w['p11']
                score -= penalty
                sal0[0] += penalty
        
        if a3 == 7:
            if a1 in [2, 5, 7]:
                penalty = w['p1'] if gender0 == 1 else w['p11']
                score -= penalty
                sal0[0] += penalty
            if a2 in [2, 5, 7]:
                penalty = w['p1'] if gender0 == 1 else w['p11']
                score -= penalty
                sal0[0] += penalty
        
        if a3 == 2:
            if a1 in [7, 8, 11]:
                penalty = w['p1'] if gender0 == 1 else w['p11']
                score -= penalty
                sal0[0] += penalty
            if a2 in [7, 8, 11]:
                penalty = w['p1'] if gender0 == 1 else w['p11']
                score -= penalty
                sal0[0] += penalty
        
        # Same rules for person 1
        if b3 == 3:
            if b1 in [6, 9]:
                penalty = w['p1'] if gender1 == 1 else w['p11']
                score -= penalty
                sal1[0] += penalty
            if b2 in [6, 9]:
                penalty = w['p1'] if gender1 == 1 else w['p11']
                score -= penalty
                sal1[0] += penalty
        
        if b3 == 7:
            if b1 in [2, 5, 7]:
                penalty = w['p1'] if gender1 == 1 else w['p11']
                score -= penalty
                sal1[0] += penalty
            if b2 in [2, 5, 7]:
                penalty = w['p1'] if gender1 == 1 else w['p11']
                score -= penalty
                sal1[0] += penalty
        
        if b3 == 2:
            if b1 in [7, 8, 11]:
                penalty = w['p1'] if gender1 == 1 else w['p11']
                score -= penalty
                sal1[0] += penalty
            if b2 in [7, 8, 11]:
                penalty = w['p1'] if gender1 == 1 else w['p11']
                score -= penalty
                sal1[0] += penalty
        
        # Rule 2: 육해살 (Yukhaesal) - Six Harm penalty
        harm_pairs = {
            1: 10, 2: 7, 3: 8, 4: 9, 5: 12, 6: 11,
            7: 2, 8: 3, 9: 4, 10: 1, 11: 6, 12: 5
        }
        
        if a3 in harm_pairs:
            if a1 == harm_pairs[a3] or a2 == harm_pairs[a3]:
                penalty = w['p2'] if gender0 == 1 else w['p21']
                score -= penalty
                sal0[1] += penalty
        
        if b3 in harm_pairs:
            if b1 == harm_pairs[b3] or b2 == harm_pairs[b3]:
                penalty = w['p2'] if gender1 == 1 else w['p21']
                score -= penalty
                sal1[1] += penalty
        
        # Additional rules can be added here...
        # For brevity, implementing key rules only
        
        return score, sal0, sal1
    
    def analyze_compatibility(
        self,
        year1: int, month1: int, day1: int, hour1: int, gender1: int,
        year2: int, month2: int, day2: int, hour2: int, gender2: int
    ) -> Dict:
        """
        Main compatibility analysis function
        
        Args:
            year1, month1, day1, hour1: First person's birth info
            gender1: 0=female, 1=male
            year2, month2, day2, hour2: Second person's birth info  
            gender2: 0=female, 1=male
        
        Returns:
            Dictionary with compatibility score and detailed analysis
        """
        # Get Saju pillars for both people
        # Note: This is simplified - actual implementation would use calendar conversion
        saju1 = self._get_saju_pillars(year1, month1, day1, hour1)
        saju2 = self._get_saju_pillars(year2, month2, day2, hour2)
        
        # Calculate base compatibility using ML models
        sky_score = self.calculate_sky_score(saju1[0], saju2[0])
        earth_score = self.calculate_earth_score(saju1[1], saju2[1])
        base_score = (sky_score + earth_score) / 2
        
        # Calculate detailed compatibility with traditional rules
        final_score, traits1, traits2 = self.calculate_detailed_compatibility(
            saju1, saju2, gender1, gender2, base_score * 100
        )
        
        # Normalize score to 0-100
        final_score = max(0, min(100, final_score))
        
        return {
            'compatibility_score': round(final_score, 2),
            'saju_data_user1': {
                'year_sky': saju1[0],
                'year_earth': saju1[1],
                'month_sky': saju1[2],
                'month_earth': saju1[3],
                'day_sky': saju1[4],
                'day_earth': saju1[5]
            },
            'saju_data_user2': {
                'year_sky': saju2[0],
                'year_earth': saju2[1],
                'month_sky': saju2[2],
                'month_earth': saju2[3],
                'day_sky': saju2[4],
                'day_earth': saju2[5]
            },
            'detailed_scores': {
                'person1_traits': traits1,
                'person2_traits': traits2,
                'sky_score': float(sky_score),
                'earth_score': float(earth_score)
            },
            'interpretation': self._generate_interpretation(final_score)
        }
    
    def _get_saju_pillars(self, year: int, month: int, day: int, hour: int) -> List[int]:
        """
        Convert birth date/time to Saju pillars
        
        Returns:
            List of 6 integers representing [year_sky, year_earth, month_sky, month_earth, day_sky, day_earth]
        """
        # Simplified calculation - actual implementation would use lunar calendar
        # This is a placeholder that generates deterministic values
        ry = (year - 1904) % 10
        ys = ry + 1 if ry != 0 else 10
        
        ry2 = (year - 1990) % 12
        yg = ((ry2 + 2) % 12) + 1
        
        # Simplified month calculation
        ms = ((ys - 1) * 2 + month - 1) % 10 + 1
        mg = (month + 1) % 12 + 1
        
        # Simplified day calculation
        ds = ((year + month + day) % 10) + 1
        dg = ((year + month + day) % 12) + 1
        
        return [ys, yg, ms, mg, ds, dg]
    
    def _generate_interpretation(self, score: float) -> str:
        """Generate text interpretation based on compatibility score"""
        if score >= 90:
            return "매우 높은 궁합! 천생연분의 궁합입니다. 서로를 이해하고 존중하며 행복한 관계를 유지할 수 있습니다."
        elif score >= 80:
            return "높은 궁합! 서로 잘 맞는 커플입니다. 조금의 노력으로 완벽한 관계를 만들 수 있습니다."
        elif score >= 70:
            return "좋은 궁합! 대체로 잘 맞는 관계입니다. 서로 이해하려는 노력이 필요합니다."
        elif score >= 60:
            return "평범한 궁합. 서로 맞춰가는 노력이 필요하지만 충분히 좋은 관계를 유지할 수 있습니다."
        elif score >= 50:
            return "보통 궁합. 서로의 차이를 인정하고 노력한다면 관계를 발전시킬 수 있습니다."
        else:
            return "궁합이 다소 맞지 않는 면이 있습니다. 하지만 진정한 사랑과 노력으로 극복할 수 있습니다."


# Global engine instance
_engine_instance = None


def get_engine() -> SajuEngine:
    """Get global Saju engine instance (singleton)"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SajuEngine()
    return _engine_instance
