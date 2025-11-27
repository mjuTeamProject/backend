# Soulmatch Backend API

Soulmatch는 AI 사주 분석 기술을 활용한 커플 애플리케이션의 백엔드 서버입니다.

## 주요 기능

- 🔐 **회원 관리**: JWT 기반 인증, 커플 연동
- 🔮 **AI 궁합 분석**: 딥러닝 기반 사주 궁합 분석
- 📊 **랭킹 시스템**: Redis 기반 실시간 랭킹
- 🎁 **보상 시스템**: 배지, 쿠폰 관리
- 📱 **SNS 공유**: 궁합 인증서 이미지 생성 및 공유

## 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **AI/ML**: TensorFlow, NumPy
- **Authentication**: JWT, Bcrypt

## 프로젝트 구조

```
backend/
├── app/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── config.py               # 설정 관리
│   ├── database.py             # 데이터베이스 연결
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── couple.py
│   │   ├── analysis.py
│   │   ├── ranking.py
│   │   └── reward.py
│   ├── schemas/                # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── couple.py
│   │   ├── analysis.py
│   │   └── ranking.py
│   ├── api/                    # API 라우터
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── couples.py
│   │   ├── analysis.py
│   │   ├── ranking.py
│   │   └── share.py
│   ├── services/               # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── analysis_service.py
│   │   ├── ranking_service.py
│   │   ├── image_service.py
│   │   └── share_service.py
│   ├── repositories/           # 데이터 액세스 레이어
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── couple_repository.py
│   │   └── analysis_repository.py
│   ├── ai/                     # AI 엔진
│   │   ├── __init__.py
│   │   ├── saju_engine.py
│   │   └── compatibility.py
│   ├── utils/                  # 유틸리티
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── validators.py
│   │   └── cache.py
│   └── middleware/             # 미들웨어
│       ├── __init__.py
│       └── error_handler.py
├── tests/                      # 테스트
├── alembic/                    # DB 마이그레이션
├── requirements.txt
├── .env.example
└── README.md
```

## 설치 및 실행

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정 (데이터베이스, Redis, JWT 시크릿 등)
```

### 3. 데이터베이스 초기화

```bash
# Alembic 마이그레이션 실행
alembic upgrade head
```

### 4. 서버 실행

```bash
# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 주요 API 엔드포인트

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/refresh` - 토큰 갱신

### 사용자
- `GET /api/users/me` - 내 정보 조회
- `PUT /api/users/me` - 프로필 수정
- `POST /api/users/partner` - 파트너 연동

### 궁합 분석
- `POST /api/analysis/calculate` - 궁합 분석 요청
- `GET /api/analysis/{id}` - 분석 결과 조회
- `GET /api/analysis/image/{id}` - 인증서 이미지 생성

### 랭킹
- `GET /api/ranking/daily` - 일간 랭킹
- `GET /api/ranking/weekly` - 주간 랭킹
- `POST /api/ranking/register` - 랭킹 등록

## 개발 가이드

### 코드 스타일
```bash
# 포맷팅
black app/

# 린팅
flake8 app/

# 타입 체크
mypy app/
```

### 테스트
```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app tests/
```

## 라이선스

Copyright Reserved by Team Mate
