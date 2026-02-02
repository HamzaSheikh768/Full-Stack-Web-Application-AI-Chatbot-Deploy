#!/usr/bin/env python3
"""
Environment checker script to verify that all required environment variables are set correctly
for the Next.js + FastAPI application to work together.
"""

import os
import sys
from dotenv import load_dotenv

def load_env_files():
    """Load environment variables from .env files"""
    # Load from project root
    root_env = load_dotenv('.env')
    print(f"Loaded root .env: {root_env}")

    # Load from backend
    backend_env = load_dotenv('../backend/.env')
    print(f"Loaded backend .env: {backend_env}")

    # Load from frontend
    frontend_env = load_dotenv('../frontend/.env')
    print(f"Loaded frontend .env: {frontend_env}")

def check_backend_env():
    """Check backend environment variables"""
    print("\nChecking backend environment variables...")

    required_vars = [
        "BETTER_AUTH_SECRET",
        "JWT_SECRET_KEY",
        "DATABASE_URL"
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"  [OK] {var}: {'SET' if value else 'MISSING'}")

    if missing_vars:
        print(f"  [ERROR] Missing required backend variables: {missing_vars}")
        return False

    # Check that BETTER_AUTH_SECRET and JWT_SECRET_KEY have the same value
    better_auth_secret = os.getenv("BETTER_AUTH_SECRET")
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")

    if better_auth_secret != jwt_secret_key:
        print(f"  [WARN] Warning: BETTER_AUTH_SECRET and JWT_SECRET_KEY differ")
        print(f"     BETTER_AUTH_SECRET: {better_auth_secret[:10]}...")
        print(f"     JWT_SECRET_KEY: {jwt_secret_key[:10]}...")
        print("     This may cause authentication issues")

    return True

def check_frontend_env():
    """Check frontend environment variables"""
    print("\nChecking frontend environment variables...")

    required_vars = [
        "NEXT_PUBLIC_API_URL",
        "NEXT_PUBLIC_BETTER_AUTH_URL"
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"  [OK] {var}: {value}")

    if missing_vars:
        print(f"  [ERROR] Missing required frontend variables: {missing_vars}")
        return False

    return True

def check_consistency():
    """Check consistency between backend and frontend configs"""
    print("\nChecking environment consistency...")

    # Check API URL consistency
    frontend_api_url = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    backend_port = os.getenv("PORT", "8000")

    print(f"  Frontend API URL: {frontend_api_url}")
    print(f"  Backend Port: {backend_port}")

    # Check if they seem compatible
    if f":{backend_port}" in frontend_api_url or backend_port == "8000":
        print("  [OK] API URL configuration looks consistent")
    else:
        print("  [WARN] Potential inconsistency between API URL and port")

    return True

def main():
    print("Environment Variables Checker for Next.js + FastAPI App")
    print("=" * 55)

    # Load environment variables from files
    load_env_files()

    backend_ok = check_backend_env()
    frontend_ok = check_frontend_env()
    consistency_ok = check_consistency()

    print(f"\nResults:")
    print(f"  Backend: {'[OK] OK' if backend_ok else '[ERROR] Issues'}")
    print(f"  Frontend: {'[OK] OK' if frontend_ok else '[ERROR] Issues'}")
    print(f"  Consistency: {'[OK] OK' if consistency_ok else '[WARN] Warnings'}")

    if not (backend_ok and frontend_ok):
        print("\n[ERROR] Some required environment variables are missing!")
        print("Please check your .env files in both frontend and backend directories.")
        sys.exit(1)
    else:
        print("\n[OK] All environment variables are properly configured!")
        return 0

if __name__ == "__main__":
    main()