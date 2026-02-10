import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from src.main import app  # Adjust import based on your app structure
from src.database.db import get_db
# Import models for type hints but not for schema creation in tests
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.user import User
else:
    # Define simplified models for testing with SQLite compatibility
    from sqlmodel import SQLModel, Field
    from typing import Optional
    from datetime import datetime
    import uuid
    import sqlalchemy as sa
    from enum import Enum
    
    class TaskPriority(str, Enum):
        low = "low"
        medium = "medium"
        high = "high"
    
    class RecurrenceEnum(str, Enum):
        none = "none"
        daily = "daily"
        weekly = "weekly"
        monthly = "monthly"
        yearly = "yearly"
    
    class Task(SQLModel, table=True):
        __tablename__ = "test_task"  # Different table name for testing
        
        id: str = Field(
            sa_column=sa.Column(
                sa.String,
                primary_key=True,
                default=lambda: str(uuid.uuid4())
            )
        )
        user_id: str = Field(sa_column=sa.Column(sa.String, nullable=False))
        parent_id: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))
        title: str = Field(sa_column=sa.Column(sa.String(256), nullable=False))
        description: Optional[str] = Field(sa_column=sa.Column(sa.String, nullable=True))
        is_completed: bool = Field(default=False, sa_column=sa.Column('is_completed', sa.Boolean, nullable=False))
        priority: str = Field(default="medium", sa_column=sa.Column(sa.String, nullable=False))
        
        # Simplified for SQLite - store as JSON string instead of ARRAY
        tags: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))  # JSON string representation
        due_date: Optional[datetime] = Field(sa_column=sa.Column(sa.DateTime, nullable=True))
        remind_at: Optional[datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime, nullable=True))
        is_recurring: bool = Field(default=False, sa_column=sa.Column(sa.Boolean, nullable=False))
        recurrence_pattern: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))  # JSON string
        next_due_date: Optional[datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime, nullable=True))
        
        order_index: Optional[str] = Field(default="0", sa_column=sa.Column(sa.String, nullable=True))
        created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sa.Column(sa.DateTime, nullable=False))
        updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sa.Column(sa.DateTime, nullable=False))
    
    class User(SQLModel, table=True):
        __tablename__ = "test_user"  # Different table name for testing
        
        id: str = Field(
            sa_column=sa.Column(
                sa.String,
                primary_key=True,
                default=lambda: str(uuid.uuid4())
            )
        )
        email: str = Field(sa_column=sa.Column(sa.String, unique=True, nullable=False))
        hashed_password: str = Field(sa_column=sa.Column(sa.String, nullable=False))
        first_name: Optional[str] = Field(sa_column=sa.Column(sa.String, nullable=True))
        last_name: Optional[str] = Field(sa_column=sa.Column(sa.String, nullable=True))
        created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sa.Column(sa.DateTime, nullable=False))
        updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=sa.Column(sa.DateTime, nullable=False))
from datetime import datetime, timedelta
import json


# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="module")
def test_app():
    """Create a test client for the FastAPI app"""
    # Override the database dependency with our test database
    def override_get_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def setup_database():
    """Set up a fresh database for each test"""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def mock_user(setup_database):
    """Create a mock user for testing"""
    # Create a session to interact with the database
    with Session(engine) as session:
        user = User(
            email="test@example.com",
            hashed_password="hashed_test_password",
            first_name="Test",
            last_name="User"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@pytest.fixture
def auth_headers(test_app, mock_user):
    """Get authentication headers for the mock user"""
    # Login to get token (adjust based on your auth implementation)
    response = test_app.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test_password"
    })

    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        # If login fails, create a mock token for testing purposes
        # In a real scenario, you'd need to adjust this based on your auth system
        return {"Authorization": "Bearer fake_token"}


def test_create_task_integration(test_app, mock_user, auth_headers):
    """Test creating a task through the API"""
    task_data = {
        "title": "Integration Test Task",
        "description": "A task created through integration test",
        "priority": "high",
        "tags": ["integration", "test"],
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "remind_at": (datetime.now() + timedelta(hours=1)).isoformat(),
        "is_recurring": False
    }
    
    response = test_app.post(
        f"/api/{mock_user.id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Integration Test Task"
    assert data["data"]["priority"] == "high"
    assert "integration" in data["data"]["tags"]
    assert "test" in data["data"]["tags"]


def test_get_tasks_integration(test_app, mock_user, auth_headers):
    """Test retrieving tasks through the API"""
    # First create a task
    task_data = {
        "title": "Get Tasks Test",
        "description": "A task for testing retrieval",
        "priority": "medium",
        "tags": ["retrieval", "test"]
    }
    
    create_response = test_app.post(
        f"/api/{mock_user.id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert create_response.status_code == 200
    
    # Now retrieve tasks
    response = test_app.get(
        f"/api/{mock_user.id}/tasks",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["tasks"]) >= 1
    # Find our test task in the response
    test_task = next((t for t in data["data"]["tasks"] if t["title"] == "Get Tasks Test"), None)
    assert test_task is not None
    assert test_task["priority"] == "medium"


def test_update_task_integration(test_app, mock_user, auth_headers):
    """Test updating a task through the API"""
    # First create a task
    task_data = {
        "title": "Original Title",
        "description": "Original description",
        "priority": "low"
    }
    
    create_response = test_app.post(
        f"/api/{mock_user.id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()["data"]
    task_id = created_task["id"]
    
    # Now update the task
    update_data = {
        "title": "Updated Title",
        "priority": "high",
        "tags": ["updated", "test"]
    }
    
    response = test_app.put(
        f"/api/{mock_user.id}/tasks/{task_id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Updated Title"
    assert data["data"]["priority"] == "high"
    assert "updated" in data["data"]["tags"]


def test_toggle_task_completion_integration(test_app, mock_user, auth_headers):
    """Test toggling task completion through the API"""
    # First create a task
    task_data = {
        "title": "Toggle Completion Test",
        "description": "Task for testing completion toggle",
        "priority": "medium"
    }
    
    create_response = test_app.post(
        f"/api/{mock_user.id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()["data"]
    task_id = created_task["id"]
    
    # Verify task is initially not completed
    assert created_task["is_completed"] is False
    
    # Toggle completion to True
    response = test_app.patch(
        f"/api/{mock_user.id}/tasks/{task_id}/complete",
        json={"is_completed": True},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_completed"] is True
    
    # Toggle completion back to False
    response = test_app.patch(
        f"/api/{mock_user.id}/tasks/{task_id}/complete",
        json={"is_completed": False},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_completed"] is False


def test_filter_and_search_tasks_integration(test_app, mock_user, auth_headers):
    """Test filtering and searching tasks through the API"""
    # Create multiple tasks with different properties
    tasks_data = [
        {
            "title": "High Priority Task",
            "description": "This is a high priority task",
            "priority": "high",
            "tags": ["important", "urgent"]
        },
        {
            "title": "Low Priority Task",
            "description": "This is a low priority task",
            "priority": "low",
            "tags": ["later", "not-urgent"]
        },
        {
            "title": "Medium Priority Task",
            "description": "This is a medium priority task",
            "priority": "medium",
            "tags": ["normal", "routine"]
        }
    ]
    
    for task_data in tasks_data:
        response = test_app.post(
            f"/api/{mock_user.id}/tasks",
            json=task_data,
            headers=auth_headers
        )
        assert response.status_code == 200
    
    # Test filtering by priority
    response = test_app.get(
        f"/api/{mock_user.id}/tasks?priority=high",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    high_priority_tasks = [t for t in data["data"]["tasks"] if t["priority"] == "high"]
    assert len(high_priority_tasks) >= 1
    
    # Test searching by keyword
    response = test_app.get(
        f"/api/{mock_user.id}/tasks?search=high",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    search_results = [t for t in data["data"]["tasks"] if "high" in t["title"].lower()]
    assert len(search_results) >= 1


def test_delete_task_integration(test_app, mock_user, auth_headers):
    """Test deleting a task through the API"""
    # First create a task
    task_data = {
        "title": "Delete Test Task",
        "description": "Task for testing deletion",
        "priority": "medium"
    }
    
    create_response = test_app.post(
        f"/api/{mock_user.id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()["data"]
    task_id = created_task["id"]
    
    # Verify task exists
    get_response = test_app.get(
        f"/api/{mock_user.id}/tasks/{task_id}",
        headers=auth_headers
    )
    
    assert get_response.status_code == 200
    
    # Delete the task
    response = test_app.delete(
        f"/api/{mock_user.id}/tasks/{task_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verify task is deleted
    get_response = test_app.get(
        f"/api/{mock_user.id}/tasks/{task_id}",
        headers=auth_headers
    )
    
    assert get_response.status_code == 404


def test_user_isolation_integration(test_app, mock_user, auth_headers):
    """Test that users can only access their own tasks"""
    # Create a task for the mock user
    task_data = {
        "title": "User Isolation Test",
        "description": "Task for testing user isolation",
        "priority": "medium"
    }
    
    create_response = test_app.post(
        f"/api/{mock_user.id}/tasks",
        json=task_data,
        headers=auth_headers
    )
    
    assert create_response.status_code == 200
    created_task = create_response.json()["data"]
    task_id = created_task["id"]
    
    # Try to access the task with a different user ID (should fail)
    different_user_id = "different_user_id_than_mock_user"
    response = test_app.get(
        f"/api/{different_user_id}/tasks/{task_id}",
        headers=auth_headers
    )
    
    # Should return 404 or 403 depending on implementation
    assert response.status_code in [403, 404]