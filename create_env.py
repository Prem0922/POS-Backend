#!/usr/bin/env python3
"""
Create .env file for POS Backend with JWT authentication
"""

import os
import secrets

def create_env_file():
    """Create .env file with all necessary environment variables"""
    env_content = """# POS Backend Environment Variables

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/pos_db

# API Keys
POS_API_KEY=pos_secret_key
CRM_API_KEY=mysecretkey

# JWT Authentication
POS_JWT_SECRET=pos_jwt_secret_key_change_in_production_12345

# CRM Backend URL
CRM_BASE_URL=https://crm-n577.onrender.com

# Server Configuration
PORT=8001
HOST=0.0.0.0
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(" Created .env file with JWT authentication configuration")
        return True
    except Exception as e:
        print(f" Failed to create .env file: {e}")
        return False

if __name__ == "__main__":
    create_env_file()
