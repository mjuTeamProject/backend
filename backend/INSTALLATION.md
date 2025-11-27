# Soulmatch Backend - 설치 및 실행 가이드

## 📋 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [초기 설정](#초기-설정)
3. [데이터베이스 설정](#데이터베이스-설정)
4. [Redis 설정](#redis-설정)
5. [서버 실행](#서버-실행)
6. [API 테스트](#api-테스트)
7. [문제 해결](#문제-해결)

## 시스템 요구사항

- Python 3.10 이상
- PostgreSQL 14 이상
- Redis 6 이상
- 최소 4GB RAM
- 최소 2GB 디스크 공간

## 초기 설정

### 1. 가상환경 생성 및 활성화

```powershell
# backend 디렉토리로 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 가상환경 활성화 (Windows CMD)
.\venv\Scripts\activate.bat
```

### 2. 의존성 설치

```powershell
# requirements.txt 패키지 설치
pip install -r requirements.txt
```

> ⚠️ **주의**: TensorFlow 설치 시 시간이 오래 걸릴 수 있습니다 (5-10분)

### 3. AI 모델 파일 복사

프로젝트 루트의 AI 모델 파일들을 backend 상위 디렉토리에 배치:

```
soulmatch/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
├── sky3000.h5          ← 이 위치
├── earth3000.h5        ← 이 위치
└── cal.csv             ← 이 위치
```

## 데이터베이스 설정

### 1. PostgreSQL 설치 및 실행

Windows에서 PostgreSQL 설치:
1. https://www.postgresql.org/download/windows/ 에서 다운로드
2. 설치 시 포트 5432 사용
3. 비밀번호 설정 (예: postgres)

### 2. 데이터베이스 생성

```powershell
# PostgreSQL 명령줄 도구 실행
psql -U postgres

# SQL 명령 실행
CREATE DATABASE soulmatch;
CREATE USER soulmatch_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE soulmatch TO soulmatch_user;
\q
```

### 3. 환경 변수 설정

`.env` 파일 생성:

```powershell
# .env.example을 .env로 복사
Copy-Item .env.example .env

# .env 파일 편집 (메모장 또는 VS Code)
notepad .env
```

`.env` 파일 내용 수정:

```env
# Application Settings
APP_NAME=Soulmatch
DEBUG=True
ENVIRONMENT=development

# Database Settings
DATABASE_URL=postgresql+asyncpg://soulmatch_user:your_password@localhost:5432/soulmatch

# Redis Settings  
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT Settings (강력한 비밀키로 변경하세요!)
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Model Settings
SKY_MODEL_PATH=../sky3000.h5
EARTH_MODEL_PATH=../earth3000.h5
CALENDAR_FILE_PATH=../cal.csv
```

### 4. 데이터베이스 마이그레이션

```powershell
# Alembic 초기화 (최초 1회만)
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

## Redis 설정

### Windows에서 Redis 설치

#### 방법 1: Docker 사용 (권장)

```powershell
# Docker Desktop 설치 후
docker run -d -p 6379:6379 --name soulmatch-redis redis:latest
```

#### 방법 2: WSL2 사용

```powershell
# WSL2에서 Ubuntu 실행
wsl

# Redis 설치
sudo apt update
sudo apt install redis-server

# Redis 시작
sudo service redis-server start

# Redis 테스트
redis-cli ping
# 응답: PONG
```

## 서버 실행

### 개발 서버 실행

```powershell
# backend 디렉토리에서
cd backend

# 가상환경이 활성화되어 있는지 확인
# 프롬프트에 (venv) 표시가 있어야 함

# Uvicorn으로 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 정상적으로 시작되면:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
✅ Soulmatch v1.0.0 started
INFO:     Application startup complete.
```

## API 테스트

### 1. 브라우저에서 API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Health Check

```powershell
# PowerShell에서
Invoke-WebRequest -Uri "http://localhost:8000/health"

# 또는 브라우저에서
# http://localhost:8000/health
```

### 3. API 테스트 예제

#### 회원가입

```powershell
$body = @{
    username = "testuser"
    password = "Test1234"
    nickname = "테스트유저"
    email = "test@example.com"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

#### 로그인

```powershell
$body = @{
    username = "testuser"
    password = "Test1234"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$token = ($response.Content | ConvertFrom-Json).access_token
```

#### 내 프로필 조회

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/users/me" `
    -Method GET `
    -Headers @{Authorization = "Bearer $token"}
```

## 문제 해결

### 1. ModuleNotFoundError

```powershell
# 가상환경이 활성화되어 있는지 확인
# 의존성 재설치
pip install -r requirements.txt
```

### 2. Database connection error

- PostgreSQL 서비스가 실행 중인지 확인
- `.env` 파일의 DATABASE_URL이 올바른지 확인
- 방화벽에서 포트 5432가 열려있는지 확인

```powershell
# PostgreSQL 서비스 상태 확인
Get-Service postgresql*

# 서비스 시작
Start-Service postgresql-x64-14
```

### 3. Redis connection error

- Redis 서버가 실행 중인지 확인

```powershell
# Docker 사용 시
docker ps | Select-String "redis"

# WSL2 사용 시
wsl -e redis-cli ping
```

### 4. TensorFlow/Model loading errors

- AI 모델 파일들이 올바른 위치에 있는지 확인
- `.env` 파일의 경로가 올바른지 확인

```powershell
# 파일 존재 확인
Test-Path ..\sky3000.h5
Test-Path ..\earth3000.h5
Test-Path ..\cal.csv
```

### 5. Port already in use

```powershell
# 포트 8000을 사용하는 프로세스 찾기
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# 프로세스 종료
Stop-Process -Id <PID>

# 또는 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

## 추가 명령어

### 데이터베이스 초기화

```powershell
# 모든 테이블 삭제 후 재생성
alembic downgrade base
alembic upgrade head
```

### 코드 포맷팅

```powershell
# Black으로 코드 포맷팅
black app/

# Flake8로 린팅
flake8 app/
```

### 로그 확인

```powershell
# 상세 로그 보기
uvicorn app.main:app --reload --log-level debug
```

## 다음 단계

1. Swagger UI에서 API 테스트
2. 프론트엔드 연동 준비
3. 추가 기능 구현 (랭킹, 이미지 생성 등)

## 도움말

문제가 계속되면 다음을 확인하세요:
- Python 버전: `python --version`
- Pip 버전: `pip --version`
- 설치된 패키지: `pip list`
- 서버 로그 확인
