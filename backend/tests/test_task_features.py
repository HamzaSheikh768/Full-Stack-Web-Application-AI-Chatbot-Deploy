"""
Test script to verify task management functionality
"""
import asyncio
import httpx
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_task_management():
    """Test task management functionality"""
    base_url = "http://localhost:8000"

    print("Testing TASKAPP task management functionality...")
    print("="*60)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # First, register a test user
        print("\n1. Registering test user...")
        try:
            register_data = {
                "email": "testuser@example.com",
                "password": "password123",
                "name": "Test User"
            }
            response = await client.post(
                f"{base_url}/api/auth/register",
                json=register_data
            )
            print(f"   Register response: {response.status_code}")

            if response.status_code == 200:
                register_result = response.json()
                token = register_result.get('access_token')

                if token:
                    print("   ✓ User registered successfully")

                    # Test task creation with authentication
                    print("\n2. Testing task creation...")
                    headers = {"Authorization": f"Bearer {token}"}

                    task_data = {
                        "title": "Test Task",
                        "description": "This is a test task",
                        "status": "pending"
                    }

                    task_response = await client.post(
                        f"{base_url}/api/tasks/tasks/",
                        json=task_data,
                        headers=headers
                    )

                    print(f"   Create task response: {task_response.status_code}")
                    if task_response.status_code == 200:
                        task_result = task_response.json()
                        task_id = task_result.get('id') or (task_result.get('data', {}) or {}).get('task', {}).get('id')
                        print("   ✓ Task created successfully")

                        # Test getting tasks
                        print("\n3. Testing task retrieval...")
                        get_response = await client.get(
                            f"{base_url}/api/tasks/tasks/",
                            headers=headers
                        )
                        print(f"   Get tasks response: {get_response.status_code}")
                        if get_response.status_code == 200:
                            print("   ✓ Tasks retrieved successfully")

                            # Test updating task
                            if task_id:
                                print("\n4. Testing task update...")
                                update_data = {
                                    "title": "Updated Test Task",
                                    "status": "completed"
                                }

                                update_response = await client.put(
                                    f"{base_url}/api/tasks/tasks/{task_id}",
                                    json=update_data,
                                    headers=headers
                                )
                                print(f"   Update task response: {update_response.status_code}")
                                if update_response.status_code == 200:
                                    print("   ✓ Task updated successfully")

                                    # Test toggling completion
                                    print("\n5. Testing task completion toggle...")
                                    toggle_response = await client.patch(
                                        f"{base_url}/api/tasks/tasks/{task_id}/complete",
                                        headers=headers
                                    )
                                    print(f"   Toggle completion response: {toggle_response.status_code}")
                                    if toggle_response.status_code == 200:
                                        print("   ✓ Task completion toggled successfully")

                                        # Test deleting task
                                        print("\n6. Testing task deletion...")
                                        delete_response = await client.delete(
                                            f"{base_url}/api/tasks/tasks/{task_id}",
                                            headers=headers
                                        )
                                        print(f"   Delete task response: {delete_response.status_code}")
                                        if delete_response.status_code == 200:
                                            print("   ✓ Task deleted successfully")

                                            print("\n🎉 All task management features are working correctly!")
                                            print("You should now be able to create, update, delete, and manage tasks in TASKAPP.")
                                            return True
                                        else:
                                            print("   ✗ Task deletion failed")
                                    else:
                                        print("   ✗ Task completion toggle failed")
                                else:
                                    print("   ✗ Task update failed")
                            else:
                                print("   ⚠ Could not get task ID for update/delete tests")
                        else:
                            print("   ✗ Task retrieval failed")
                    else:
                        print("   ✗ Task creation failed")
                        print(f"   Error: {task_response.text}")
                else:
                    print("   ✗ No token returned from registration")
            else:
                print("   ✗ User registration failed")
                print(f"   Error: {response.text}")

        except Exception as e:
            print(f"   ✗ Error during testing: {e}")
            print("   Note: The backend server might still be initializing. Please wait 1-2 minutes and try again.")

    print("\n⚠ Some or all task management features may not be working yet.")
    print("This could be because the backend server is still initializing the database.")
    print("Please wait a few minutes for the server to fully start and try again.")
    return False

if __name__ == "__main__":
    asyncio.run(test_task_management())