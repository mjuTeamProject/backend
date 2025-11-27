"""
API 테스트 스크립트

백엔드 API 엔드포인트를 테스트하는 스크립트입니다.
서버가 http://localhost:8000 에서 실행 중이어야 합니다.
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_health():
    """헬스 체크"""
    print("\n=== Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    """회원가입 테스트"""
    print("\n=== User Registration ===")
    data = {
        "username": "user1",
        "email": "user1@test.com",
        "password": "Test1234",
        "nickname": "testuser1"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"User ID: {result.get('user_id')}")
        print(f"Access Token: {result.get('access_token')[:50]}...")
        return result
    else:
        print(f"Error: {response.text}")
        return None

def test_login():
    """로그인 테스트"""
    print("\n=== User Login ===")
    data = {
        "username": "user1",
        "password": "Test1234"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"User ID: {result.get('user_id')}")
        print(f"Access Token: {result.get('access_token')[:50]}...")
        return result
    else:
        print(f"Error: {response.text}")
        return None

def test_get_profile(token):
    """프로필 조회 테스트"""
    print("\n=== Get Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Username: {result.get('username')}")
        print(f"Email: {result.get('email')}")
        print(f"Name: {result.get('profile', {}).get('name')}")
        return result
    else:
        print(f"Error: {response.text}")
        return None

def test_ranking():
    """랭킹 조회 테스트"""
    print("\n=== Get Rankings ===")
    
    response = requests.get(f"{BASE_URL}/api/ranking/daily")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total rankings: {len(result.get('rankings', []))}")
        return result
    else:
        print(f"Error: {response.text}")
        return None

def test_compatibility_analysis(token):
    """궁합 분석 테스트"""
    print("\n=== Compatibility Analysis ===")
    
    # 분석 데이터
    data = {
        "user1_birth_date": "1995-05-15",
        "user1_birth_time": "14:30",
        "user1_is_lunar": False,
        "user2_birth_date": "1997-08-20",
        "user2_birth_time": "09:45",
        "user2_is_lunar": False
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/analysis/calculate", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n💖 궁합 분석 결과:")
        print(f"  총점: {result.get('total_score')}점")
        print(f"  천간 점수: {result.get('sky_score')}점")
        print(f"  지지 점수: {result.get('earth_score')}점")
        print(f"  등급: {result.get('compatibility_level')}")
        print(f"  설명: {result.get('description')}")
        return result
    else:
        print(f"Error: {response.text}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Soulmatch API 테스트 시작")
    print("=" * 60)
    
    # 1. Health Check
    if not test_health():
        print("\n❌ 서버가 응답하지 않습니다. 서버가 실행 중인지 확인하세요.")
        exit(1)
    
    # 2. 회원가입
    register_result = test_register()
    
    # 3. 로그인 (회원가입 실패시에도 기존 계정으로 로그인 시도)
    login_result = test_login()
    
    if login_result:
        token = login_result.get("access_token")
        
        # 4. 프로필 조회
        test_get_profile(token)
        
        # 5. 궁합 분석 (AI 모델 사용)
        print("\n🔮 궁합 분석 테스트를 시작합니다...")
        test_compatibility_analysis(token)
    
    # 6. 랭킹 조회 (인증 불필요)
    test_ranking()
    
    print("\n" + "=" * 60)
    print("✅ API 테스트 완료!")
    print("=" * 60)
    print("\n더 많은 API 테스트는 Swagger UI에서 확인하세요:")
    print("👉 http://localhost:8001/docs")
