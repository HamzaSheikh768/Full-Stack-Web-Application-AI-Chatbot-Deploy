"""
Complete functionality test for TASKAPP
"""
import requests
import time
import sys
import os

def test_full_functionality():
    base_url = "http://localhost:8000"

    print("🔍 Testing TASKAPP Full Functionality")
    print("="*50)

    # Test 1: Health Check
    print("\n✅ Test 1: Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("   ✓ Health check passed")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Health check failed: {e}")
        return False

    # Test 2: Register User
    print("\n✅ Test 2: User Registration")
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=user_data,
            timeout=30  # Longer timeout for database initialization
        )
        if response.status_code == 200:
            print("   ✓ User registration successful")
            token_data = response.json()
            access_token = token_data.get('access_token')
        else:
            print(f"   ✗ User registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ User registration failed: {e}")
        return False

    # Test 3: Login User
    print("\n✅ Test 3: User Login")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ User login successful")
            token_data = response.json()
            access_token = token_data.get('access_token')
        else:
            print(f"   ✗ User login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ User login failed: {e}")
        return False

    # Test 4: Get User Profile
    print("\n✅ Test 4: Get User Profile")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{base_url}/api/auth/me",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Get user profile successful")
        else:
            print(f"   ✗ Get user profile failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Get user profile failed: {e}")
        return False

    # Test 5: Create Task
    print("\n✅ Test 5: Create Task")
    try:
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending"
        }
        response = requests.post(
            f"{base_url}/api/tasks/tasks/",
            json=task_data,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Task creation successful")
            task = response.json()
            task_id = task.get('id')
        else:
            print(f"   ✗ Task creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Task creation failed: {e}")
        return False

    # Test 6: Get Task
    print("\n✅ Test 6: Get Task")
    try:
        response = requests.get(
            f"{base_url}/api/tasks/tasks/{task_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Get task successful")
        else:
            print(f"   ✗ Get task failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Get task failed: {e}")
        return False

    # Test 7: Update Task
    print("\n✅ Test 7: Update Task")
    try:
        update_data = {
            "title": "Updated Test Task",
            "status": "completed"
        }
        response = requests.put(
            f"{base_url}/api/tasks/tasks/{task_id}",
            json=update_data,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Task update successful")
        else:
            print(f"   ✗ Task update failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Task update failed: {e}")
        return False

    # Test 8: Toggle Task Completion
    print("\n✅ Test 8: Toggle Task Completion")
    try:
        response = requests.patch(
            f"{base_url}/api/tasks/tasks/{task_id}/complete",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Task completion toggle successful")
        else:
            print(f"   ✗ Task completion toggle failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Task completion toggle failed: {e}")
        return False

    # Test 9: Get All Tasks
    print("\n✅ Test 9: Get All Tasks")
    try:
        response = requests.get(
            f"{base_url}/api/tasks/tasks/",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Get all tasks successful")
        else:
            print(f"   ✗ Get all tasks failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Get all tasks failed: {e}")
        return False

    # Test 10: Delete Task
    print("\n✅ Test 10: Delete Task")
    try:
        response = requests.delete(
            f"{base_url}/api/tasks/tasks/{task_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✓ Task deletion successful")
        else:
            print(f"   ✗ Task deletion failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Task deletion failed: {e}")
        return False

    print("\n🎉 All tests passed! TASKAPP is fully functional!")
    return True

if __name__ == "__main__":
    success = test_full_functionality()
    if success:
        print("\n✅ TASKAPP is ready for use!")
    else:
        print("\n❌ Some tests failed. Please check the server and try again.")