#!/usr/bin/env python3
"""
Create Admin User for POS System
"""

import requests
import json

# POS Backend URL
BASE_URL = "http://localhost:8001"

def create_admin_user():
    """Create an admin user for the POS system"""
    print("Creating admin user for POS system...")
    
    admin_data = {
        "username": "admin",
        "email": "admin@pos.com",
        "password": "admin123",
        "full_name": "POS Administrator",
        "role": "admin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=admin_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Admin user created successfully!")
            print(f"Username: {admin_data['username']}")
            print(f"Password: {admin_data['password']}")
            print(f"Role: {admin_data['role']}")
        else:
            print(f"❌ Failed to create admin user: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_manager_user():
    """Create a manager user for the POS system"""
    print("\nCreating manager user for POS system...")
    
    manager_data = {
        "username": "manager",
        "email": "manager@pos.com",
        "password": "manager123",
        "full_name": "POS Manager",
        "role": "manager"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=manager_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Manager user created successfully!")
            print(f"Username: {manager_data['username']}")
            print(f"Password: {manager_data['password']}")
            print(f"Role: {manager_data['role']}")
        else:
            print(f"❌ Failed to create manager user: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Create default users"""
    print("🚀 Creating Default POS Users")
    print("=" * 50)
    
    # Create admin user
    admin_success = create_admin_user()
    
    # Create manager user
    manager_success = create_manager_user()
    
    print("\n" + "=" * 50)
    print("📊 User Creation Results:")
    print(f"Admin User: {'✅ PASS' if admin_success else '❌ FAIL'}")
    print(f"Manager User: {'✅ PASS' if manager_success else '❌ FAIL'}")
    
    if admin_success and manager_success:
        print("\n🎉 All default users created successfully!")
        print("\n📋 Default Login Credentials:")
        print("Admin - Username: admin, Password: admin123")
        print("Manager - Username: manager, Password: manager123")
        print("Cashier - Username: test_cashier, Password: password123")

if __name__ == "__main__":
    main()
