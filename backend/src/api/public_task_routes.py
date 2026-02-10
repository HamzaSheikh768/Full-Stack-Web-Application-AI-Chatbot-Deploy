from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database.db import get_db
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from pydantic import BaseModel
from sqlmodel import select
from ..models.task import Task

router = APIRouter(prefix="/public", tags=["public-tasks"])

@router.get("/tasks", response_model=dict)
def get_all_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering (public access).
    """
    try:
        # Build query for all tasks
        from sqlmodel import select
        from sqlalchemy import and_, or_

        query = select(Task)

        # Apply optional filters
        filters = []
        if status:
            if status.lower() == "completed":
                filters.append(Task.is_completed == True)
            elif status.lower() == "pending":
                filters.append(Task.is_completed == False)

        if priority:
            filters.append(Task.priority == priority.lower())

        if search:
            filters.append(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%") if search else False
                )
            )

        if filters:
            query = query.where(and_(*filters))

        # Apply ordering and pagination
        query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)

        result = db.execute(query)
        tasks = result.scalars().all()

        # Get total count for pagination
        count_query = select(Task)
        if filters:
            count_query = count_query.where(and_(*filters))
        count_result = db.execute(count_query)
        total_count = count_result.scalar()

        # Convert to response format
        task_list = [
            {
                "id": str(task.id),
                "user_id": str(task.user_id),
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "recurrence_pattern": task.recurrence_pattern,
                "order_index": task.order_index,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

        return {
            "success": True,
            "data": {
                "tasks": task_list,
                "total": total_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID (public access).
    """
    try:
        from sqlmodel import select

        statement = select(Task).where(Task.id == task_id)
        result = db.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Convert to response format
        task_response = {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "is_completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "recurrence_pattern": task.recurrence_pattern,
            "order_index": task.order_index,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

        return task_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")

@router.get("/tasks/search", response_model=List[TaskResponse])
def search_tasks(
    q: str,
    db: Session = Depends(get_db)
):
    """
    Search tasks by title or description (public access).
    """
    try:
        from sqlmodel import select
        from sqlalchemy import or_

        query = select(Task).where(
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%") if q else False
            )
        )

        result = db.execute(query)
        tasks = result.scalars().all()

        # Convert to response format
        task_list = [
            {
                "id": str(task.id),
                "user_id": str(task.user_id),
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "recurrence_pattern": task.recurrence_pattern,
                "order_index": task.order_index,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

        return task_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tasks: {str(e)}")


@router.get("/test", response_model=Dict[str, Any])
def test_endpoint():
    """
    Simple test endpoint to verify public routes work.
    """
    return {"success": True, "message": "Public route is working!"}


@router.get("/health-check", response_model=dict)
def health_check():
    """
    Health check endpoint that definitely does not require auth.
    """
    return {"status": "healthy", "message": "Public route working"}