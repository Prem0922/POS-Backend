#!/usr/bin/env python3

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def check_postgresql_installed():
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL is installed")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed or not in PATH")
        return False

def create_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="password"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='pos_db'")
        exists = cursor.fetchone()
        
        if exists:
            print("✅ Database 'pos_db' already exists")
        else:
            cursor.execute("CREATE DATABASE pos_db")
            print("✅ Database 'pos_db' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        print("\n📋 Troubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if the password is correct")
        print("3. Verify PostgreSQL is listening on port 5432")
        return False
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def test_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="password",
            database="pos_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ Successfully connected to 'pos_db' database")
        print(f"   PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to 'pos_db' database: {e}")
        return False

def create_env_file():
    env_content = """# POS Backend Environment Variables

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/pos_db

# API Keys
POS_API_KEY=pos_secret_key
CRM_API_KEY=mysecretkey

# CRM Backend URL
CRM_BASE_URL=https://crm-n577.onrender.com

# Server Configuration
PORT=8001
HOST=0.0.0.0
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with PostgreSQL configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    print("🚀 PostgreSQL Setup for POS Backend")
    print("=" * 50)
    
    if not check_postgresql_installed():
        print("\n📥 To install PostgreSQL:")
        print("1. Download from: https://www.postgresql.org/download/")
        print("2. During installation, set password as 'password'")
        print("3. Keep default port as 5432")
        print("4. Run this script again after installation")
        return
    
    print("\n🔧 Setting up database...")
    
    if not create_database():
        return
    
    if not test_connection():
        return
    
    if not create_env_file():
        return
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Install Python dependencies: pip install -r requirements.txt")
    print("2. Run the server: python main.py")
    print("3. Test the API: python test_api.py")

if __name__ == "__main__":
    main() 