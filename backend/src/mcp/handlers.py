from sqlmodel import select
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import logging

from ..database.db import SessionLocal
from ..models.task import Task
from ..models.conversation import Conversation, Message

# Set up logging
logger = logging.getLogger(__name__)

def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = "MEDIUM",
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    remind_at: Optional[str] = None,
    is_recurring: Optional[bool] = False,
    recurrence_pattern: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a new task for the user with advanced features.
    Validates user_id ownership and persists to DB.

    Args:
        user_id: User identifier
        title: Task title
        description: Task description
        priority: Priority level (LOW, MEDIUM, HIGH)
        tags: List of tags/categories
        due_date: Due date in ISO format
        remind_at: Reminder time in ISO format
        is_recurring: Whether task should recur
        recurrence_pattern: Recurrence pattern configuration
    """
    try:
        with SessionLocal() as session:
            # Parse datetime strings if provided
            due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00')) if due_date else None
            remind_at_obj = datetime.fromisoformat(remind_at.replace('Z', '+00:00')) if remind_at else None

            # Calculate next_due_date for recurring tasks
            next_due_date_obj = None
            if is_recurring and recurrence_pattern and due_date_obj:
                from ..utils import calculate_next_occurrence
                next_due_date_obj = calculate_next_occurrence(due_date_obj, recurrence_pattern)

            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False,
                priority=priority.upper() if priority else "MEDIUM",
                tags=tags or [],
                due_date=due_date_obj,
                remind_at=remind_at_obj,
                is_recurring=is_recurring or False,
                recurrence_pattern=recurrence_pattern,
                next_due_date=next_due_date_obj
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            logger.info(f"Task created successfully: {task.id} for user: {user_id}")
            return task.model_dump()
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        return {
            "error": "Failed to create task",
            "user_id": user_id,
            "error_detail": str(e)
        }

def list_tasks(
    user_id: str,
    status: str = "all",
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> List[Dict[str, Any]]:
    """
    Retrieve tasks for the user with advanced filtering and sorting.
    Validates user_id ownership.

    Args:
        user_id: User identifier
        status: Filter by status (all, pending, completed)
        priority: Filter by priority level
        tags: Filter by tags (tasks must have at least one matching tag)
        search: Search keyword in title or description
        sort_by: Field to sort by (created_at, due_date, priority, title)
        sort_order: Sort order (asc, desc)
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            # Apply priority filter
            if priority:
                query = query.where(Task.priority == priority.upper())

            # Apply tags filter (tasks with any matching tag)
            if tags and len(tags) > 0:
                from sqlalchemy import any_
                query = query.where(Task.tags.overlap(tags))

            # Apply search filter (full-text search on title and description)
            if search:
                search_expr = f"%{search}%"
                from sqlalchemy import or_, and_
                query = query.where(
                    or_(
                        Task.title.ilike(search_expr),
                        and_(Task.description.is_not(None), Task.description.ilike(search_expr))
                    )
                )

            # Apply sorting
            if sort_by == "due_date":
                if sort_order == "asc":
                    query = query.order_by(Task.due_date.asc().nullslast())
                else:
                    query = query.order_by(Task.due_date.desc().nullslast())
            elif sort_by == "priority":
                # Sort by priority: HIGH > MEDIUM > LOW
                from sqlalchemy import case
                priority_order = case(
                    (Task.priority == "HIGH", 1),
                    (Task.priority == "MEDIUM", 2),
                    (Task.priority == "LOW", 3),
                    else_=4
                )
                if sort_order == "asc":
                    query = query.order_by(priority_order.asc())
                else:
                    query = query.order_by(priority_order.desc())
            elif sort_by == "title":
                if sort_order == "asc":
                    query = query.order_by(Task.title.asc())
                else:
                    query = query.order_by(Task.title.desc())
            else:  # Default to created_at
                if sort_order == "asc":
                    query = query.order_by(Task.created_at.asc())
                else:
                    query = query.order_by(Task.created_at.desc())

            result = session.execute(query)
            tasks = result.scalars().all()

            task_list = [t.model_dump() for t in tasks]
            logger.info(f"Retrieved {len(task_list)} tasks for user: {user_id}")
            return task_list
    except Exception as e:
        logger.error(f"Error listing tasks for user {user_id}: {str(e)}")
        return {
            "error": "Failed to retrieve tasks",
            "user_id": user_id,
            "error_detail": str(e)
        }

def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a specific task as completed.
    If the task is recurring, automatically generate the next instance.
    Validates user_id ownership and task existence.
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Task {task_id} not found for user: {user_id}")
                return {
                    "error": f"Task with ID {task_id} not found for your account",
                    "user_id": user_id,
                    "task_id": task_id
                }

            # Mark as completed
            task.completed = True
            task.updated_at = datetime.now(timezone.utc)
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task {task_id} marked as completed for user: {user_id}")

            # Generate next instance if recurring
            next_task_info = None
            if task.is_recurring and task.recurrence_pattern:
                from ..services.recurring_service import generate_recurring_task_instance
                result = generate_recurring_task_instance(user_id, str(task_id))
                if result.get("status") == "generated":
                    next_task_info = {
                        "next_task_id": result.get("new_task_id"),
                        "next_due_date": result.get("next_due_date")
                    }
                    logger.info(f"Generated next recurring task instance: {result.get('new_task_id')}")

            response = task.model_dump()
            if next_task_info:
                response["recurring_info"] = next_task_info

            return response

    except Exception as e:
        logger.error(f"Error completing task {task_id} for user {user_id}: {str(e)}")
        return {
            "error": "Failed to complete task",
            "user_id": user_id,
            "task_id": task_id,
            "error_detail": str(e)
        }

def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Permanently remove a task.
    Validates user_id ownership and task existence.
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Attempt to delete non-existent task {task_id} for user: {user_id}")
                return {
                    "error": f"Task with ID {task_id} not found for your account",
                    "user_id": user_id,
                    "task_id": task_id
                }

            session.delete(task)
            session.commit()

            logger.info(f"Task {task_id} deleted successfully for user: {user_id}")
            return {
                "status": "deleted",
                "id": task_id,
                "title": task.title
            }
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
        return {
            "error": "Failed to delete task",
            "user_id": user_id,
            "task_id": task_id,
            "error_detail": str(e)
        }

def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    remind_at: Optional[str] = None,
    is_recurring: Optional[bool] = None,
    recurrence_pattern: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Modify an existing task with advanced features.
    Validates user_id ownership and task existence.

    Args:
        user_id: User identifier
        task_id: Task identifier
        title: New task title
        description: New task description
        priority: New priority level
        tags: New tags list
        due_date: New due date in ISO format
        remind_at: New reminder time in ISO format
        is_recurring: New recurring status
        recurrence_pattern: New recurrence pattern
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Attempt to update non-existent task {task_id} for user: {user_id}")
                return {
                    "error": f"Task with ID {task_id} not found for your account",
                    "user_id": user_id,
                    "task_id": task_id
                }

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority.upper()
            if tags is not None:
                task.tags = tags
            if due_date is not None:
                task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            if remind_at is not None:
                task.remind_at = datetime.fromisoformat(remind_at.replace('Z', '+00:00'))
            if is_recurring is not None:
                task.is_recurring = is_recurring
            if recurrence_pattern is not None:
                task.recurrence_pattern = recurrence_pattern

            # Recalculate next_due_date if recurring settings changed
            if (is_recurring or task.is_recurring) and task.due_date:
                from ..utils import calculate_next_occurrence
                pattern = recurrence_pattern if recurrence_pattern is not None else task.recurrence_pattern
                if pattern:
                    task.next_due_date = calculate_next_occurrence(task.due_date, pattern)

            task.updated_at = datetime.now(timezone.utc)
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task {task_id} updated successfully for user: {user_id}")
            return task.model_dump()
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
        return {
            "error": "Failed to update task",
            "user_id": user_id,
            "task_id": task_id,
            "error_detail": str(e)
        }