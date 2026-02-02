from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from uuid import UUID
import uuid

from ..database.db import get_db
from ..models.task import Task
from ..schemas import TaskCreate, TaskUpdate, TaskResponse
from ..auth import get_current_user

router = APIRouter(tags=["tasks"])

@router.get("/{user_id}/tasks", response_model=dict)
def get_user_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Get all tasks for the specified user with optional filtering.
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    try:
        from sqlmodel import select
        from sqlalchemy import and_, or_

        # Build query with authenticated user's ID
        query = select(Task).where(Task.user_id == current_user["user_id"])

        # Apply optional filters
        filters = []
        if status_filter:
            if status_filter.lower() == "completed":
                filters.append(Task.completed == True)
            elif status_filter.lower() == "pending":
                filters.append(Task.completed == False)

        if priority:
            filters.append(Task.priority == priority.lower())

        if search:
            filters.append(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%")
                )
            )

        if filters:
            query = query.where(and_(*filters))

        # Apply ordering and pagination
        query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)

        result = db.execute(query)
        tasks = result.scalars().all()  # Use scalars() to get model instances

        # Convert to response format
        task_list = [
            {
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
            for task in tasks
        ]

        # Get total count for pagination
        from sqlalchemy import func
        count_query = select(func.count(Task.id)).where(Task.user_id == current_user["user_id"])
        if filters:
            count_query = count_query.where(and_(*filters))
        count_result = db.execute(count_query)
        total_count = count_result.scalar()

        return {
            "success": True,
            "data": {
                "tasks": task_list,
                "total": total_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")


@router.post("/{user_id}/tasks", response_model=dict)
def create_user_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the specified user.
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only create tasks for yourself"
        )

    try:
        # Create task with authenticated user's ID
        task = Task(
            user_id=current_user["user_id"],
            title=task_data.title,
            description=task_data.description,
            completed=getattr(task_data, 'completed', getattr(task_data, 'is_completed', False)),
            priority=getattr(task_data, 'priority', 'medium'),
            due_date=getattr(task_data, 'due_date', None),
            recurrence_pattern=getattr(task_data, 'recurrence_pattern', 'none'),
            order_index=getattr(task_data, 'order_index', '0')
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "data": {
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
        }
    except Exception as e:
        if hasattr(db, 'rollback'):
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/{user_id}/tasks/{task_id}", response_model=dict)
def get_user_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID for the specified user.
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    try:
        from sqlmodel import select

        # Get task and verify it belongs to the authenticated user
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user["user_id"]
        )
        result = db.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "data": {
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
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")


@router.put("/{user_id}/tasks/{task_id}", response_model=dict)
def update_user_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific task by ID for the specified user.
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    try:
        from sqlmodel import select

        # Get task and verify it belongs to the authenticated user
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user["user_id"]
        )
        result = db.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update task fields
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)

        task.updated_at = datetime.now(timezone.utc)
        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "data": {
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
        }
    except HTTPException:
        raise
    except Exception as e:
        if hasattr(db, 'rollback'):
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@router.delete("/{user_id}/tasks/{task_id}", response_model=dict)
def delete_user_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific task by ID for the specified user.
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only delete your own tasks"
        )

    try:
        from sqlmodel import select

        # Get task and verify it belongs to the authenticated user
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user["user_id"]
        )
        result = db.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()

        return {
            "success": True,
            "data": {"message": "Task deleted successfully"}
        }
    except HTTPException:
        raise
    except Exception as e:
        if hasattr(db, 'rollback'):
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=dict)
def toggle_task_completion(
    user_id: str,
    task_id: str,
    is_completed: bool = Body(..., embed=True),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle completion status of a specific task for the specified user.
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    try:
        from sqlmodel import select

        # Get task and verify it belongs to the authenticated user
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user["user_id"]
        )
        result = db.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update completion status
        task.completed = is_completed
        task.updated_at = datetime.now(timezone.utc)
        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "success": True,
            "data": {
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
        }
    except HTTPException:
        raise
    except Exception as e:
        if hasattr(db, 'rollback'):
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task completion: {str(e)}")