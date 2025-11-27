"""
Simple test server to verify FastAPI installation
간단한 테스트 서버 - FastAPI 설치 확인용
"""
from fastapi import FastAPI

app = FastAPI(title="Soulmatch Test Server")

@app.get("/")
async def root():
    return {
        "message": "✅ Soulmatch 백엔드 서버가 정상적으로 작동하고 있습니다!",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test")
async def test():
    return {
        "message": "테스트 성공!",
        "info": "프론트엔드 팀원들이 사용할 API가 준비되었습니다."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
