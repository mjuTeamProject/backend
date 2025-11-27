# Soulmatch Backend - 프로젝트 개요

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   ├── config.py               # 환경 설정
│   ├── database.py             # 데이터베이스 연결 및 세션 관리
│   │
│   ├── models/                 # SQLAlchemy ORM 모델
│   │   ├── __init__.py
│   │   ├── user.py            # User, Profile 모델
│   │   ├── couple.py          # Couple 모델
│   │   ├── analysis.py        # AnalysisRequest, AnalysisResult 모델
│   │   ├── ranking.py         # RankingEntry 모델
│   │   ├── reward.py          # Badge, Coupon, Event 모델
│   │   └── share.py           # ShareLog 모델
│   │
│   ├── schemas/                # Pydantic 스키마 (요청/응답)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── couple.py
│   │   ├── analysis.py
│   │   └── ranking.py
│   │
│   ├── api/                    # API 라우터
│   │   ├── __init__.py
│   │   ├── auth.py            # 인증 (회원가입, 로그인)
│   │   ├── users.py           # 사용자 관리
│   │   ├── couples.py         # 커플 연동
│   │   ├── analysis.py        # 궁합 분석
│   │   ├── ranking.py         # 랭킹 시스템
│   │   └── share.py           # SNS 공유
│   │
│   ├── services/               # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── auth_service.py    # 인증 서비스
│   │   ├── user_service.py    # 사용자 서비스
│   │   └── analysis_service.py # 분석 서비스
│   │
│   ├── repositories/           # 데이터 액세스 레이어
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── couple_repository.py
│   │   └── analysis_repository.py
│   │
│   ├── ai/                     # AI 엔진
│   │   ├── __init__.py
│   │   └── saju_engine.py     # 사주 분석 엔진
│   │
│   └── utils/                  # 유틸리티
│       ├── __init__.py
│       ├── security.py        # JWT, 비밀번호 해싱
│       ├── validators.py      # 입력 검증
│       └── cache.py           # Redis 캐싱
│
├── tests/                      # 테스트 코드
├── alembic/                    # 데이터베이스 마이그레이션
├── requirements.txt            # Python 의존성
├── .env.example                # 환경 변수 템플릿
├── .gitignore
├── README.md
└── INSTALLATION.md             # 설치 가이드
```

## ✅ 구현 완료 기능

### 1. 회원 관리 시스템 ✅
- **회원가입/로그인**: JWT 기반 인증
- **프로필 관리**: 닉네임, 이메일, 생년월일시 등
- **커플 연동**: 파트너와 1:1 연결
- **보안**: Bcrypt 비밀번호 암호화, JWT 토큰

**API 엔드포인트:**
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/refresh` - 토큰 갱신
- `GET /api/users/me` - 내 정보 조회
- `PUT /api/users/me` - 프로필 수정
- `POST /api/couples/connect` - 파트너 연동
- `DELETE /api/couples/disconnect` - 파트너 연결 해제

### 2. AI 궁합 분석 엔진 ✅
- **사주 분석**: 생년월일시 기반 사주 계산
- **딥러닝 모델**: TensorFlow 기반 천간/지지 궁합 분석
- **상세 분석**: 8가지 성향 분석 (공망살, 육해살 등)
- **해석 생성**: 점수별 자동 해석 메시지

**API 엔드포인트:**
- `POST /api/analysis/calculate` - 궁합 분석 실행
- `GET /api/analysis/{result_id}` - 분석 결과 조회
- `GET /api/analysis/couple/{couple_id}/history` - 분석 이력 조회

### 3. 데이터베이스 구조 ✅
- **Users**: 사용자 기본 정보
- **Profiles**: 사용자 상세 프로필 (생년월일시, 성별 등)
- **Couples**: 커플 관계
- **AnalysisRequests**: 분석 요청 기록
- **AnalysisResults**: 분석 결과 저장
- **RankingEntries**: 랭킹 데이터
- **Badges, Coupons, Events**: 보상 시스템
- **ShareLogs**: 공유 기록

## 🚧 진행 중 / 예정 기능

### 4. 결과 시각화 및 이미지 생성 (예정)
- 궁합 인증서 이미지 자동 생성
- Pillow/Matplotlib 기반 이미지 렌더링
- 캐싱을 통한 성능 최적화

### 5. 랭킹 시스템 (예정)
- Redis Sorted Set 기반 실시간 랭킹
- 일간/주간/월간 랭킹
- 어뷰징 방지 로직

### 6. 보상 및 이벤트 시스템 (예정)
- 배지 시스템
- 쿠폰 발급 및 관리
- 이벤트 관리

### 7. SNS 공유 기능 (예정)
- 카카오톡, 인스타그램 공유
- 공유 로그 기록
- 바이럴 효과 추적

## 🔧 기술 스택

### Backend Framework
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **Python 3.10+**: 타입 힌팅, 비동기 프로그래밍

### Database
- **PostgreSQL**: 메인 데이터베이스
- **SQLAlchemy**: ORM
- **Alembic**: 마이그레이션

### Caching & Session
- **Redis**: 캐싱, 세션, 랭킹 데이터

### AI/ML
- **TensorFlow**: 딥러닝 모델
- **NumPy**: 수치 계산
- **Pandas**: 데이터 처리

### Authentication & Security
- **JWT**: JSON Web Tokens
- **Bcrypt**: 비밀번호 해싱
- **python-jose**: JWT 구현

### Image Processing (예정)
- **Pillow**: 이미지 생성
- **Matplotlib**: 차트/그래프

## 📊 데이터 흐름

```
User Request
    ↓
API Router (auth.py, users.py, analysis.py, etc.)
    ↓
Service Layer (비즈니스 로직)
    ↓
Repository Layer (데이터 액세스)
    ↓
Database / AI Engine
    ↓
Response
```

## 🔐 인증 흐름

```
1. 회원가입/로그인
   → Bcrypt로 비밀번호 해싱
   → JWT 액세스 토큰 + 리프레시 토큰 발급

2. API 요청
   → Authorization 헤더에 Bearer 토큰 포함
   → get_current_user 의존성으로 토큰 검증
   → User 객체 반환

3. 토큰 갱신
   → 리프레시 토큰으로 새 액세스 토큰 발급
```

## 🧮 궁합 분석 흐름

```
1. 사용자가 파트너와 연동
2. 양쪽 프로필에 생년월일시 입력
3. POST /api/analysis/calculate 호출
4. AnalysisService:
   - 커플 정보 및 프로필 검증
   - SajuEngine으로 분석 요청
5. SajuEngine:
   - 사주 팔자 계산
   - ML 모델로 천간/지지 궁합 점수 계산
   - 전통 규칙으로 상세 분석
   - 해석 텍스트 생성
6. 결과 DB 저장 및 반환
```

## 🎯 API 엔드포인트 요약

| 기능 | Method | Endpoint | 인증 |
|------|--------|----------|------|
| 회원가입 | POST | `/api/auth/register` | ❌ |
| 로그인 | POST | `/api/auth/login` | ❌ |
| 토큰 갱신 | POST | `/api/auth/refresh` | ❌ |
| 내 정보 조회 | GET | `/api/users/me` | ✅ |
| 프로필 수정 | PUT | `/api/users/me` | ✅ |
| 상세 프로필 수정 | PUT | `/api/users/me/profile` | ✅ |
| 파트너 정보 | GET | `/api/users/me/partner` | ✅ |
| 파트너 연동 | POST | `/api/couples/connect` | ✅ |
| 파트너 해제 | DELETE | `/api/couples/disconnect` | ✅ |
| 궁합 분석 | POST | `/api/analysis/calculate` | ✅ |
| 분석 결과 조회 | GET | `/api/analysis/{result_id}` | ✅ |
| 분석 이력 | GET | `/api/analysis/couple/{couple_id}/history` | ✅ |
| 일간 랭킹 | GET | `/api/ranking/daily` | ❌ |
| 주간 랭킹 | GET | `/api/ranking/weekly` | ❌ |
| 랭킹 등록 | POST | `/api/ranking/register` | ✅ |

## 📝 사용 예제

### 1. 전체 워크플로우

```bash
# 1. 회원가입 (두 명의 사용자)
POST /api/auth/register
{
  "username": "user1",
  "password": "User1234",
  "nickname": "김철수"
}

POST /api/auth/register
{
  "username": "user2",
  "password": "User2234",
  "nickname": "이영희"
}

# 2. 프로필 업데이트 (생년월일시 입력)
PUT /api/users/me/profile
{
  "birth_year": 1995,
  "birth_month": 3,
  "birth_day": 15,
  "birth_hour": 14,
  "gender": "male"
}

# 3. 파트너 연동
POST /api/couples/connect
{
  "partner_username": "user2"
}

# 4. 궁합 분석
POST /api/analysis/calculate

# 5. 결과 조회
GET /api/analysis/{result_id}
```

## 🛠️ 개발 가이드

### 새로운 API 엔드포인트 추가

1. **Schema 정의** (`app/schemas/`)
2. **Model 정의** (`app/models/`) - 필요시
3. **Repository 추가** (`app/repositories/`)
4. **Service 로직 구현** (`app/services/`)
5. **Router 추가** (`app/api/`)
6. **main.py에 Router 등록**

### 데이터베이스 변경

```bash
# 1. 모델 수정
# 2. 마이그레이션 생성
alembic revision --autogenerate -m "설명"

# 3. 마이그레이션 적용
alembic upgrade head
```

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [PostgreSQL 문서](https://www.postgresql.org/docs/)
- [Redis 문서](https://redis.io/documentation)
- [TensorFlow 문서](https://www.tensorflow.org/api_docs)
