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

def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for the user.
    Validates user_id ownership and persists to DB.
    """
    try:
        with SessionLocal() as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False  # New tasks are not completed by default
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

def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    Retrieve tasks for the user, optionally filtered by status.
    Validates user_id ownership.
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.user_id == user_id)

            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            result = session.execute(query)
            tasks = result.scalars().all()

            task_list = [t.model_dump() for t in tasks]
            logger.info(f"Retrieved {len(task_list)} tasks for user: {user_id} with status: {status}")
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

            task.completed = True
            task.updated_at = datetime.now(timezone.utc)
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task {task_id} marked as completed for user: {user_id}")
            return task.model_dump()
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

def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Modify the title or description of an existing task.
    Validates user_id ownership and task existence.
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