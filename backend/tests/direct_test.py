"""
Direct test to verify the authentication functionality
"""
import asyncio
import aiohttp
import sys
import os

async def test_direct_connection():
    """Test direct connection to backend"""
    print("Testing direct connection to backend...")

    # Test GET request to root endpoint
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            print("Testing / endpoint...")
            async with session.get('http://localhost:8000/') as response:
                print(f"Root endpoint: Status {response.status}")
                data = await response.json()
                print(f"Response: {data}")

            print("\nTesting /health endpoint...")
            async with session.get('http://localhost:8000/health') as response:
                print(f"Health endpoint: Status {response.status}")
                data = await response.json()
                print(f"Response: {data}")

            print("\nTesting /docs endpoint...")
            async with session.get('http://localhost:8000/docs') as response:
                print(f"Docs endpoint: Status {response.status}")
                print(f"Headers: Content-Type={response.content_type}")

    except Exception as e:
        print(f"Connection error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_connection())