import requests
import json

BASE_URL = "http://localhost:8001"
API_KEY = "pos_secret_key"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_card_balance():
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}/api/cards/4716000000000001/balance", headers=headers)
        print(f"Card Balance: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Card balance test failed: {e}")
        return False

def test_reports_summary():
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}/api/reports/summary", headers=headers)
        print(f"Reports Summary: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Reports summary test failed: {e}")
        return False

def test_customer_lookup():
    try:
        headers = {"x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}/api/customers/CUST000001", headers=headers)
        print(f"Customer Lookup: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Customer lookup test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing POS Backend API Endpoints...")
    print("=" * 50)
    
    health_ok = test_health()
    root_ok = test_root()
    
    if health_ok and root_ok:
        print("\n✅ Basic endpoints working!")
        
        print("\nTesting API endpoints...")
        card_balance_ok = test_card_balance()
        reports_ok = test_reports_summary()
        customer_ok = test_customer_lookup()
        
        if card_balance_ok and reports_ok and customer_ok:
            print("\n🎉 All API endpoints working correctly!")
        else:
            print("\n⚠️ Some API endpoints failed")
    else:
        print("\n❌ Basic endpoints failed - server may not be running") 