"""
CRUD operations for Task entity
Handles all database operations for tasks with proper async support
"""

from sqlmodel import select
from ..models import Task
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from ..schemas import TaskCreate, TaskUpdate
from datetime import datetime
from ..exceptions import TaskNotFoundException, InvalidTaskDataException, DatabaseOperationException
import json


async def get_tasks_by_user_id(
    session,
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    """
    Retrieve all tasks for a specific user with optional filtering, search, and sorting
    """
    try:
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status is not None:
            query = query.where(Task.status == status)

        # Apply priority filter
        if priority is not None:
            query = query.where(Task.priority == priority)

        # Apply search filter (across title and description)
        if search is not None:
            search_expr = f"%{search}%"
            from sqlalchemy import or_, and_
            query = query.where(
                or_(
                    Task.title.ilike(search_expr),
                    and_(Task.description.is_not(None), Task.description.ilike(search_expr))
                )
            )

        # Apply date range filter
        if date_from is not None:
            query = query.where(Task.created_at >= date_from)
        if date_to is not None:
            query = query.where(Task.created_at <= date_to)

        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "asc":
                query = query.order_by(Task.due_date.asc())
            else:
                query = query.order_by(Task.due_date.desc())
        elif sort_by == "created_at":
            if sort_order == "asc":
                query = query.order_by(Task.created_at.asc())
            else:
                query = query.order_by(Task.created_at.desc())
        elif sort_by == "priority":
            if sort_order == "asc":
                query = query.order_by(Task.priority.asc())
            else:
                query = query.order_by(Task.priority.desc())
        elif sort_by == "title":
            if sort_order == "asc":
                query = query.order_by(Task.title.asc())
            else:
                query = query.order_by(Task.title.desc())
        else:
            if sort_order == "asc":
                query = query.order_by(Task.title.asc())
            else:
                query = query.order_by(Task.title.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await session.execute(query)
        tasks = result.scalars().all()

        return tasks
    except Exception as e:
        raise DatabaseOperationException(detail=f"Failed to retrieve tasks: {str(e)}")


async def get_task_by_id_and_user(session, task_id: str, user_id: str):
    """
    Retrieve a specific task by ID for a specific user
    """
    try:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise TaskNotFoundException(task_id)

        return task
    except TaskNotFoundException:
        raise
    except Exception as e:
        raise DatabaseOperationException(detail=f"Failed to retrieve task: {str(e)}")


async def create_task(session, task_data: TaskCreate, user_id: str):
    """
    Create a new task for a specific user
    """
    try:
        # Create task data dictionary
        task_dict = task_data.model_dump()  # Updated from dict() to model_dump() for Pydantic v2
        task_dict["user_id"] = user_id
        # Set default status if not provided
        if "status" not in task_dict or task_dict["status"] is None:
            task_dict["status"] = "pending"

        # Create task instance
        task = Task(**task_dict)

        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except IntegrityError:
        raise InvalidTaskDataException(detail="Task data violates database constraints")
    except Exception as e:
        raise DatabaseOperationException(detail=f"Failed to create task: {str(e)}")


async def update_task(session, task_id: str, user_id: str, task_update: TaskUpdate):
    """
    Update a specific task for a specific user
    """
    try:
        # Get the existing task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise TaskNotFoundException(task_id)

        # Update task with provided fields
        update_data = task_update.model_dump(exclude_unset=True)  # Updated from dict() to model_dump()

        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(task)
        return task
    except TaskNotFoundException:
        raise
    except Exception as e:
        raise DatabaseOperationException(detail=f"Failed to update task: {str(e)}")


async def delete_task(session, task_id: str, user_id: str):
    """
    Delete a specific task for a specific user
    """
    try:
        # Get the task to delete
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise TaskNotFoundException(task_id)

        await session.delete(task)
        await session.commit()
        return True
    except TaskNotFoundException:
        raise
    except Exception as e:
        raise DatabaseOperationException(detail=f"Failed to delete task: {str(e)}")


async def toggle_task_completion(session, task_id: str, user_id: str, status: Optional[str] = None):
    """
    Toggle the status of a specific task for a specific user
    If the task is recurring and being marked as completed, create a new recurring instance
    """
    try:
        # Get the existing task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise TaskNotFoundException(task_id)

        # Update status
        original_status = task.status
        if status is not None:
            task.status = status
        else:
            # Toggle the status between 'pending' and 'completed'
            if task.status == 'completed':
                task.status = 'pending'
            else:
                task.status = 'completed'

        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        # Handle recurrence if the task is being marked as completed
        new_task_instance = None
        if original_status != 'completed' and task.status == 'completed' and task.recurrence_pattern != 'none':
            # Task is being marked as completed and it's a recurring task
            # Create a new instance for the next occurrence
            from ..utils import calculate_next_occurrence
            next_due_date = calculate_next_occurrence(task.due_date, task.recurrence_pattern.value if hasattr(task.recurrence_pattern, 'value') else task.recurrence_pattern)

            # Create new task with same properties but reset to pending
            new_task = Task(
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=False,
                due_date=next_due_date,
                priority=task.priority,
                recurrence_pattern=task.recurrence_pattern,
                tags=task.tags,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(new_task)
            await session.flush()  # Get the new task ID without committing
            new_task_instance = new_task

        await session.commit()
        await session.refresh(task)

        # Return both the updated task and the new recurring instance if created
        return task, new_task_instance
    except TaskNotFoundException:
        raise
    except Exception as e:
        raise DatabaseOperationException(detail=f"Failed to toggle task status: {str(e)}")