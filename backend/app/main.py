from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.api import auth, users, couples, analysis, ranking, share


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    await init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started")
    yield
    # Shutdown
    print(f"🛑 {settings.APP_NAME} shutting down")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI 사주 분석 기반 커플 애플리케이션 백엔드 API",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(couples.router, prefix="/api/couples", tags=["Couples"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(ranking.router, prefix="/api/ranking", tags=["Ranking"])
app.include_router(share.router, prefix="/api/share", tags=["Share"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
