# Soulmatch Backend 사용 가이드

## 📋 목차
1. [개발 환경 설정](#개발-환경-설정)
2. [서버 실행 방법](#서버-실행-방법)
3. [API 테스트 방법](#api-테스트-방법)
4. [주요 API 사용 예시](#주요-api-사용-예시)
5. [데이터베이스 관리](#데이터베이스-관리)
6. [문제 해결](#문제-해결)

---

## 개발 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/mjuTeamProject/backend.git
cd backend
```

### 2. 가상환경 생성 및 활성화

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 입력:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./soulmatch.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Models
SKY_MODEL_PATH=./models/sky3000.h5
EARTH_MODEL_PATH=./models/earth3000.h5
CALENDAR_FILE_PATH=./models/cal.csv

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 5. 데이터베이스 초기화
```bash
alembic upgrade head
```

---

## 서버 실행 방법

### 개발 모드 (자동 리로드)
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프로덕션 모드
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 서버 확인
브라우저에서 다음 URL 접속:
- API 문서: http://localhost:8000/docs
- 대체 문서: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

## API 테스트 방법

### Swagger UI 사용 (권장)

1. **브라우저에서 접속**: http://localhost:8000/docs

2. **사용자 등록** (`POST /api/auth/register`)
   - "Try it out" 클릭
   - Request body 입력:
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "Test1234",
     "password_confirm": "Test1234"
   }
   ```
   - "Execute" 클릭

3. **로그인** (`POST /api/auth/login`)
   - Request body:
   ```json
   {
     "username": "testuser",
     "password": "Test1234"
   }
   ```
   - 응답에서 `access_token` 복사

4. **인증 설정**
   - 페이지 상단 "Authorize" 🔓 버튼 클릭
   - 복사한 토큰 붙여넣기
   - "Authorize" 클릭 → "Close"

5. **프로필 업데이트** (`PUT /api/users/me/profile`)
   ```json
   {
     "birth_year": 1995,
     "birth_month": 5,
     "birth_day": 15,
     "birth_hour": 14,
     "gender": "M",
     "lunar_calendar": false
   }
   ```

6. **궁합 분석** (`POST /api/analysis/calculate`)
   - 두 명의 사용자가 커플로 연결된 후 실행
   - Request body는 비워두기 (현재 로그인한 사용자 자동 사용)

---

## 주요 API 사용 예시

### 1. 사용자 관리

#### 회원가입
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123",
    "password_confirm": "Password123"
  }'
```

#### 로그인
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "Password123"
  }'
```

응답:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### 내 정보 조회
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. 프로필 관리

#### 프로필 업데이트
```bash
curl -X PUT "http://localhost:8000/api/users/me/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_year": 1995,
    "birth_month": 3,
    "birth_day": 15,
    "birth_hour": 10,
    "gender": "M",
    "lunar_calendar": false
  }'
```

### 3. 커플 관리

#### 파트너 연결
```bash
curl -X POST "http://localhost:8000/api/couples/connect" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_username": "user2"
  }'
```

#### 커플 정보 조회
```bash
curl -X GET "http://localhost:8000/api/couples/my" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. 궁합 분석

#### 분석 실행
```bash
curl -X POST "http://localhost:8000/api/analysis/calculate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

응답 예시:
```json
{
  "id": 1,
  "couple_id": 1,
  "compatibility_score": 85.5,
  "saju_data_user1": {
    "year_sky": "갑",
    "year_earth": "자",
    "month_sky": "병",
    "month_earth": "인"
  },
  "saju_data_user2": {
    "year_sky": "을",
    "year_earth": "축",
    "month_sky": "정",
    "month_earth": "묘"
  },
  "detailed_scores": {
    "sky_score": 0.85,
    "earth_score": 0.86,
    "person1_traits": "...",
    "person2_traits": "..."
  },
  "interpretation": "궁합이 매우 좋습니다...",
  "created_at": "2025-11-27T13:00:00"
}
```

#### 분석 결과 조회
```bash
curl -X GET "http://localhost:8000/api/analysis/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 커플의 분석 이력 조회
```bash
curl -X GET "http://localhost:8000/api/analysis/couple/1/history" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 데이터베이스 관리

### 마이그레이션 생성
스키마를 변경한 후:
```bash
alembic revision --autogenerate -m "변경 내용 설명"
```

### 마이그레이션 적용
```bash
alembic upgrade head
```

### 마이그레이션 롤백
```bash
alembic downgrade -1
```

### 데이터베이스 초기화 (주의: 모든 데이터 삭제)
```bash
# 데이터베이스 파일 삭제
rm soulmatch.db  # Linux/Mac
del soulmatch.db  # Windows

# 마이그레이션 재적용
alembic upgrade head
```

---

## 문제 해결

### 포트가 이미 사용 중인 경우

**Windows:**
```powershell
# 포트 8000 사용 중인 프로세스 확인
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# 프로세스 종료
Stop-Process -Id <프로세스ID> -Force
```

**Mac/Linux:**
```bash
# 포트 8000 사용 중인 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>
```

또는 다른 포트 사용:
```bash
uvicorn app.main:app --reload --port 8001
```

### "Module not found" 에러
```bash
# 가상환경 활성화 확인
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

### 데이터베이스 에러
```bash
# 마이그레이션 상태 확인
alembic current

# 최신 마이그레이션 적용
alembic upgrade head

# 문제가 계속되면 데이터베이스 재생성
rm soulmatch.db
alembic upgrade head
```

### AI 모델 파일 에러
```
Error: No file or directory found at ./models/sky3000.h5
```

해결 방법:
1. `models/` 폴더에 다음 파일이 있는지 확인:
   - `sky3000.h5`
   - `earth3000.h5`
   - `cal.csv`
2. 없으면 저장소에서 다시 클론하거나 파일 복사

### CORS 에러 (프론트엔드 연동 시)
`.env` 파일의 `ALLOWED_ORIGINS`에 프론트엔드 URL 추가:
```env
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173","http://your-frontend-url"]
```

---

## 테스트 시나리오 예시

### 완전한 플로우 테스트

1. **사용자 A 등록 및 로그인**
```bash
# 회원가입
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"Alice123","password_confirm":"Alice123"}'

# 로그인
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"Alice123"}'
# 토큰 저장: TOKEN_A=...
```

2. **사용자 B 등록 및 로그인**
```bash
# 회원가입
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@example.com","password":"Bob123","password_confirm":"Bob123"}'

# 로그인
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"Bob123"}'
# 토큰 저장: TOKEN_B=...
```

3. **프로필 설정**
```bash
# Alice 프로필
curl -X PUT http://localhost:8000/api/users/me/profile \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"birth_year":1995,"birth_month":5,"birth_day":15,"birth_hour":10,"gender":"F","lunar_calendar":false}'

# Bob 프로필
curl -X PUT http://localhost:8000/api/users/me/profile \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{"birth_year":1993,"birth_month":8,"birth_day":20,"birth_hour":14,"gender":"M","lunar_calendar":false}'
```

4. **커플 연결**
```bash
# Alice가 Bob과 연결
curl -X POST http://localhost:8000/api/couples/connect \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"partner_username":"bob"}'
```

5. **궁합 분석**
```bash
curl -X POST http://localhost:8000/api/analysis/calculate \
  -H "Authorization: Bearer $TOKEN_A"
```

---

## 추가 리소스

- **Swagger API 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc
- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **Alembic 문서**: https://alembic.sqlalchemy.org/

## 팀원을 위한 Quick Start

```bash
# 1. 저장소 클론
git clone https://github.com/mjuTeamProject/backend.git
cd backend

# 2. 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. 패키지 설치
pip install -r requirements.txt

# 4. .env 파일 생성 (위의 예시 참고)

# 5. 데이터베이스 초기화
alembic upgrade head

# 6. 서버 실행
uvicorn app.main:app --reload

# 7. 브라우저에서 http://localhost:8000/docs 접속
```

끝!
