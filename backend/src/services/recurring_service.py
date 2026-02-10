"""
Recurring Task Generator Service
Handles automatic generation of next task instances for recurring tasks
"""

from sqlmodel import select
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import logging

from ..database.db import SessionLocal
from ..models.task import Task
from ..utils import calculate_next_occurrence

# Set up logging
logger = logging.getLogger(__name__)


def generate_recurring_task_instance(user_id: str, completed_task_id: str) -> Dict[str, Any]:
    """
    Generate the next instance of a recurring task when the current one is completed.

    This function is called when a recurring task is marked as completed.
    It creates a new task instance with the same properties but updated due dates.

    Args:
        user_id: User identifier for ownership validation
        completed_task_id: ID of the task that was just completed

    Returns:
        Dict containing the new task data or error information
    """
    try:
        with SessionLocal() as session:
            # Get the completed task
            query = select(Task).where(Task.id == completed_task_id, Task.user_id == user_id)
            result = session.execute(query)
            completed_task = result.scalar_one_or_none()

            if not completed_task:
                logger.warning(f"Task {completed_task_id} not found for user: {user_id}")
                return {
                    "error": f"Task with ID {completed_task_id} not found",
                    "user_id": user_id,
                    "task_id": completed_task_id
                }

            # Check if task is recurring
            if not completed_task.is_recurring or not completed_task.recurrence_pattern:
                logger.info(f"Task {completed_task_id} is not recurring, skipping generation")
                return {
                    "status": "skipped",
                    "reason": "Task is not recurring",
                    "task_id": completed_task_id
                }

            # Calculate next due date
            if not completed_task.next_due_date:
                logger.warning(f"Task {completed_task_id} has no next_due_date, calculating from due_date")
                if completed_task.due_date:
                    next_due = calculate_next_occurrence(completed_task.due_date, completed_task.recurrence_pattern)
                else:
                    logger.error(f"Task {completed_task_id} has no due_date, cannot generate next instance")
                    return {
                        "error": "Cannot generate recurring task without due_date",
                        "task_id": completed_task_id
                    }
            else:
                next_due = completed_task.next_due_date

            # Check if recurrence has ended
            if not next_due:
                logger.info(f"Recurrence ended for task {completed_task_id}")
                return {
                    "status": "ended",
                    "reason": "Recurrence pattern has ended",
                    "task_id": completed_task_id
                }

            # Calculate the due date after this one
            next_next_due = calculate_next_occurrence(next_due, completed_task.recurrence_pattern)

            # Calculate remind_at for new instance if original had one
            new_remind_at = None
            if completed_task.remind_at and completed_task.due_date:
                # Calculate the time difference between original remind_at and due_date
                time_diff = completed_task.due_date - completed_task.remind_at
                # Apply same difference to new due date
                new_remind_at = next_due - time_diff

            # Create new task instance
            new_task = Task(
                user_id=user_id,
                title=completed_task.title,
                description=completed_task.description,
                completed=False,
                priority=completed_task.priority,
                tags=completed_task.tags,
                due_date=next_due,
                remind_at=new_remind_at,
                is_recurring=True,
                recurrence_pattern=completed_task.recurrence_pattern,
                next_due_date=next_next_due,
                order_index=completed_task.order_index
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            logger.info(f"Generated new recurring task instance {new_task.id} from {completed_task_id}")

            return {
                "status": "generated",
                "original_task_id": completed_task_id,
                "new_task_id": str(new_task.id),
                "new_task": new_task.model_dump(),
                "next_due_date": next_due.isoformat() if next_due else None
            }

    except Exception as e:
        logger.error(f"Error generating recurring task for {completed_task_id}: {str(e)}")
        return {
            "error": "Failed to generate recurring task",
            "user_id": user_id,
            "task_id": completed_task_id,
            "error_detail": str(e)
        }


def check_and_generate_overdue_recurring_tasks(user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Check for recurring tasks that should have generated new instances but haven't.
    This is a cleanup function to handle cases where task completion didn't trigger generation.

    Args:
        user_id: Optional user ID to limit check to specific user

    Returns:
        Dict containing count of generated tasks and details
    """
    try:
        with SessionLocal() as session:
            # Build query for recurring tasks with next_due_date in the past
            query = select(Task).where(
                Task.is_recurring == True,
                Task.next_due_date.is_not(None),
                Task.next_due_date <= datetime.now(timezone.utc),
                Task.completed == True  # Only completed tasks should generate new instances
            )

            if user_id:
                query = query.where(Task.user_id == user_id)

            result = session.execute(query)
            overdue_tasks = result.scalars().all()

            generated_count = 0
            generated_tasks = []

            for task in overdue_tasks:
                # Generate new instance
                result = generate_recurring_task_instance(task.user_id, str(task.id))
                if result.get("status") == "generated":
                    generated_count += 1
                    generated_tasks.append(result)

            logger.info(f"Generated {generated_count} overdue recurring task instances")

            return {
                "status": "success",
                "checked_count": len(overdue_tasks),
                "generated_count": generated_count,
                "generated_tasks": generated_tasks
            }

    except Exception as e:
        logger.error(f"Error checking overdue recurring tasks: {str(e)}")
        return {
            "error": "Failed to check overdue recurring tasks",
            "error_detail": str(e)
        }
