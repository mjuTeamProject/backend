"""
Test converted models with real saju compatibility analysis
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_converted_models():
    """Test compatibility analysis with converted models"""
    
    print("="*60)
    print("Testing Converted ML Models")
    print("="*60)
    
    # 1. Login as user1
    print("\n1. Logging in as user1...")
    login_response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        data={
            "username": "user1",
            "password": "password123"
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Logged in successfully")
    
    # 2. Request compatibility analysis
    print("\n2. Requesting compatibility analysis...")
    
    # Get couple ID first
    couples_response = requests.get(
        f"{BASE_URL}/api/v1/couples/my-couples",
        headers=headers
    )
    
    if couples_response.status_code != 200 or not couples_response.json():
        print("❌ No couple connection found")
        return
    
    couple_id = couples_response.json()[0]["id"]
    print(f"✓ Found couple ID: {couple_id}")
    
    # Request analysis
    analysis_response = requests.post(
        f"{BASE_URL}/api/v1/analysis/analyze/{couple_id}",
        headers=headers
    )
    
    if analysis_response.status_code != 200:
        print(f"❌ Analysis failed: {analysis_response.status_code}")
        print(analysis_response.text)
        return
    
    result = analysis_response.json()
    print("\n" + "="*60)
    print("Analysis Results:")
    print("="*60)
    print(f"Overall Score: {result['overall_score']}/100")
    print(f"Sky Score: {result['sky_score']}")
    print(f"Earth Score: {result['earth_score']}")
    print(f"\nDetailed Scores:")
    for key, value in result.items():
        if key.endswith('_score') and key not in ['overall_score', 'sky_score', 'earth_score']:
            print(f"  {key}: {value}")
    
    # Check if scores are reasonable (not all 0.9999 or 0)
    if result['overall_score'] > 0 and result['overall_score'] < 100:
        print("\n✅ Model appears to be working correctly!")
        print("   Scores are in reasonable range")
    else:
        print("\n⚠ Warning: Scores might indicate untrained model")
    
    return result

if __name__ == '__main__':
    test_converted_models()
