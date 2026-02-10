"""
Reminder Service
Handles reminder notifications for tasks with remind_at timestamps
"""

from sqlmodel import select
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
import logging

from ..database.db import SessionLocal
from ..models.task import Task

# Set up logging
logger = logging.getLogger(__name__)


def check_due_reminders(user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Check for tasks with reminders that are due now or in the past.

    This function should be called periodically (e.g., every minute) to check
    for tasks that need reminder notifications.

    Args:
        user_id: Optional user ID to limit check to specific user

    Returns:
        Dict containing list of tasks with due reminders
    """
    try:
        with SessionLocal() as session:
            # Build query for tasks with remind_at in the past or now
            current_time = datetime.now(timezone.utc)

            query = select(Task).where(
                Task.remind_at.is_not(None),
                Task.remind_at <= current_time,
                Task.completed == False  # Only remind for incomplete tasks
            )

            if user_id:
                query = query.where(Task.user_id == user_id)

            result = session.execute(query)
            due_reminders = result.scalars().all()

            reminder_list = []
            for task in due_reminders:
                reminder_list.append({
                    "task_id": str(task.id),
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "remind_at": task.remind_at.isoformat() if task.remind_at else None,
                    "priority": task.priority,
                    "tags": task.tags or []
                })

            logger.info(f"Found {len(reminder_list)} due reminders")

            return {
                "status": "success",
                "count": len(reminder_list),
                "reminders": reminder_list
            }

    except Exception as e:
        logger.error(f"Error checking due reminders: {str(e)}")
        return {
            "error": "Failed to check due reminders",
            "error_detail": str(e)
        }


def get_upcoming_reminders(user_id: str, hours_ahead: int = 24) -> Dict[str, Any]:
    """
    Get upcoming reminders for a user within the specified time window.

    Args:
        user_id: User identifier
        hours_ahead: Number of hours to look ahead (default: 24)

    Returns:
        Dict containing list of upcoming reminders
    """
    try:
        with SessionLocal() as session:
            current_time = datetime.now(timezone.utc)
            future_time = current_time + timedelta(hours=hours_ahead)

            query = select(Task).where(
                Task.user_id == user_id,
                Task.remind_at.is_not(None),
                Task.remind_at > current_time,
                Task.remind_at <= future_time,
                Task.completed == False
            ).order_by(Task.remind_at.asc())

            result = session.execute(query)
            upcoming_tasks = result.scalars().all()

            reminder_list = []
            for task in upcoming_tasks:
                # Calculate time until reminder
                time_until = task.remind_at - current_time
                hours_until = time_until.total_seconds() / 3600

                reminder_list.append({
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "remind_at": task.remind_at.isoformat(),
                    "hours_until": round(hours_until, 1),
                    "priority": task.priority,
                    "tags": task.tags or []
                })

            logger.info(f"Found {len(reminder_list)} upcoming reminders for user {user_id}")

            return {
                "status": "success",
                "count": len(reminder_list),
                "reminders": reminder_list,
                "time_window_hours": hours_ahead
            }

    except Exception as e:
        logger.error(f"Error getting upcoming reminders for user {user_id}: {str(e)}")
        return {
            "error": "Failed to get upcoming reminders",
            "user_id": user_id,
            "error_detail": str(e)
        }


def send_reminder_notification(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Send a reminder notification for a specific task.

    This is a placeholder function that should be integrated with your
    notification system (email, push notifications, etc.)

    Args:
        task_id: Task identifier
        user_id: User identifier

    Returns:
        Dict containing notification status
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                return {
                    "error": f"Task with ID {task_id} not found",
                    "user_id": user_id,
                    "task_id": task_id
                }

            # TODO: Integrate with actual notification system
            # For now, just log the notification
            notification_message = f"Reminder: {task.title}"
            if task.due_date:
                notification_message += f" (Due: {task.due_date.strftime('%Y-%m-%d %H:%M')})"

            logger.info(f"Sending reminder notification to user {user_id}: {notification_message}")

            # In a real implementation, this would:
            # 1. Send push notification via Firebase/OneSignal
            # 2. Send email via SendGrid/AWS SES
            # 3. Create in-app notification
            # 4. Publish event to Dapr pub/sub for notification service

            return {
                "status": "sent",
                "task_id": task_id,
                "user_id": user_id,
                "notification_message": notification_message,
                "sent_at": datetime.now(timezone.utc).isoformat()
            }

    except Exception as e:
        logger.error(f"Error sending reminder notification for task {task_id}: {str(e)}")
        return {
            "error": "Failed to send reminder notification",
            "task_id": task_id,
            "user_id": user_id,
            "error_detail": str(e)
        }


def clear_reminder(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Clear the reminder for a task (set remind_at to None).

    This can be called after a reminder has been sent or if the user
    wants to cancel the reminder.

    Args:
        task_id: Task identifier
        user_id: User identifier

    Returns:
        Dict containing operation status
    """
    try:
        with SessionLocal() as session:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                logger.warning(f"Task {task_id} not found for user {user_id}")
                return {
                    "error": f"Task with ID {task_id} not found",
                    "user_id": user_id,
                    "task_id": task_id
                }

            task.remind_at = None
            task.updated_at = datetime.now(timezone.utc)
            session.add(task)
            session.commit()

            logger.info(f"Cleared reminder for task {task_id}")

            return {
                "status": "cleared",
                "task_id": task_id,
                "user_id": user_id
            }

    except Exception as e:
        logger.error(f"Error clearing reminder for task {task_id}: {str(e)}")
        return {
            "error": "Failed to clear reminder",
            "task_id": task_id,
            "user_id": user_id,
            "error_detail": str(e)
        }
