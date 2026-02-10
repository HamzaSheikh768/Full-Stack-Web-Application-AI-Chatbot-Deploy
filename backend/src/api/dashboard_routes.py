from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
from ..database.db import get_db
from ..models.user import User
from ..models.task import Task

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=Dict[str, Any])
def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics (public access).
    """
    try:
        # Get all tasks from the database for aggregate statistics
        # Use raw SQL to avoid model mismatches with the database schema
        from sqlalchemy import text
        
        # Select only the columns that existed in the original schema
        query = text("""
            SELECT id, user_id, title, description, completed, priority, due_date, 
                   created_at, updated_at, order_index, parent_id, remind_at, 
                   is_recurring, recurrence_pattern, next_due_date
            FROM task
        """)
        result = db.execute(query)
        rows = result.fetchall()
        
        # Calculate statistics based on the retrieved data
        total_tasks = len(rows)
        
        # Count completed tasks
        completed_tasks = sum(1 for row in rows if row.completed)
        pending_tasks = total_tasks - completed_tasks

        # Count tasks by recurrence pattern
        task_types = {"daily": 0, "weekly": 0, "monthly": 0, "yearly": 0, "none": 0}
        for row in rows:
            recurrence_pattern = getattr(row, 'recurrence_pattern', 'none') or 'none'
            if recurrence_pattern and str(recurrence_pattern) in task_types:
                task_types[str(recurrence_pattern)] += 1

        # Count tasks by priority
        task_priorities = {"low": 0, "medium": 0, "high": 0}
        for row in rows:
            priority = getattr(row, 'priority', 'medium') or 'medium'
            if priority and str(priority).lower() in task_priorities:
                task_priorities[str(priority).lower()] += 1

        return {
            "success": True,
            "data": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "task_types": task_types,
                "task_priorities": task_priorities
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dashboard stats: {str(e)}")