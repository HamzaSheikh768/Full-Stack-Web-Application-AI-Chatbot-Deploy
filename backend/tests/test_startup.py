"""
Quick test to check if the app can be imported without initialization issues
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_import():
    try:
        print("Testing app import...")
        from src.main import app
        print("[OK] App imported successfully")

        print("Testing database connection...")
        import asyncio
        from src.database.db import async_engine

        async def test_conn():
            async with async_engine.connect() as conn:
                print("[OK] Database connection successful")

        asyncio.run(test_conn())

        print("[OK] All imports successful - app should start properly")

    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_import()