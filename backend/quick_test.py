"""빠른 API 테스트"""
import requests
import time

BASE_URL = "http://localhost:8001"

# 1. 로그인
print("로그인 중...")
login_data = {
    "username": "user1",
    "password": "Test1234"
}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"로그인 응답: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    token = result["access_token"]
    print(f"토큰: {token[:50]}...")
    
    # 2. 프로필 업데이트
    print("\n프로필 업데이트 중...")
    profile_data = {
        "birth_year": 1995,
        "birth_month": 5,
        "birth_day": 15,
        "birth_hour": 14,
        "gender": "male"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{BASE_URL}/api/users/me/profile", json=profile_data, headers=headers)
    print(f"프로필 업데이트 응답: {response.status_code}")
    print(f"응답 내용: {response.json()}")
    
else:
    print(f"로그인 실패: {response.text}")
