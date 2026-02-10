from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy import or_
from sqlalchemy.sql import func
from ..models.task import Task, TaskPriority, RecurrenceEnum
from ..models.user import User
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"  # Will be mapped to is_completed in database
    priority: str = "medium"
    type: str = "daily"      # Will be mapped to recurrence_pattern in database
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # Will be mapped to is_completed in database
    priority: Optional[str] = None
    type: Optional[str] = None    # Will be mapped to recurrence_pattern in database
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: str  # Convert UUID to string for API response
    title: str
    description: Optional[str]
    status: str  # Will be derived from is_completed in database
    priority: str
    type: str    # Will be derived from recurrence_pattern in database
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user_id: str


class TaskService:
    @staticmethod
    async def create_task(task_data: TaskCreate, user_id: str, session: AsyncSession) -> TaskResponse:
        # Create new task with field mapping:
        # API 'status' -> DB 'is_completed' (convert "completed"/"pending" to boolean)
        # API 'type' -> DB 'recurrence_pattern'
        is_completed = (task_data.status.lower() == "completed")
        recurrence_pattern = task_data.type.lower() if task_data.type else None

        db_task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=is_completed,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        # Return response with status mapping:
        # DB 'completed' -> API 'status' (convert boolean to "completed"/"pending")
        status = "completed" if db_task.completed else "pending"

        return TaskResponse(
            id=str(db_task.id),  # Convert to string
            title=db_task.title,
            description=db_task.description,
            status=status,
            priority="medium",  # Default priority since not in DB model
            type="daily",      # Default type since not in DB model
            due_date=None,     # Default due_date since not in DB model
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            user_id=str(db_task.user_id)  # Convert to string
        )

    @staticmethod
    async def get_task_by_id_public(task_id: str, session: AsyncSession) -> Optional[TaskResponse]:
        statement = select(Task).where(Task.id == task_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if task:
            # Map database fields to API response:
            # DB 'completed' -> API 'status' (convert boolean to "completed"/"pending")
            status = "completed" if task.completed else "pending"

            return TaskResponse(
                id=str(task.id),  # Convert to string
                title=task.title,
                description=task.description,
                status=status,
                priority="medium",  # Default priority since not in DB model
                type="daily",      # Default type since not in DB model
                due_date=None,     # Default due_date since not in DB model
                created_at=task.created_at,
                updated_at=task.updated_at,
                user_id=str(task.user_id)  # Convert to string
            )
        return None

    @staticmethod
    async def get_task_by_id(task_id: str, user_id: str, session: AsyncSession) -> Optional[TaskResponse]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if task:
            # Map database fields to API response:
            # DB 'completed' -> API 'status' (convert boolean to "completed"/"pending")
            status = "completed" if task.completed else "pending"

            return TaskResponse(
                id=str(task.id),  # Convert to string
                title=task.title,
                description=task.description,
                status=status,
                priority="medium",  # Default priority since not in DB model
                type="daily",      # Default type since not in DB model
                due_date=None,     # Default due_date since not in DB model
                created_at=task.created_at,
                updated_at=task.updated_at,
                user_id=str(task.user_id)  # Convert to string
            )
        return None

    @staticmethod
    async def get_all_tasks(session: AsyncSession,
                           status: Optional[str] = None,
                           limit: int = 100,
                           offset: int = 0) -> List[TaskResponse]:
        statement = select(Task)

        # Map status filter to is_completed field
        if status:
            is_completed_filter = (status.lower() == "completed")
            statement = statement.where(Task.is_completed == is_completed_filter)

        statement = statement.offset(offset).limit(limit)

        result = await session.execute(statement)
        tasks = result.scalars().all()

        return [
            TaskResponse(
                id=str(task.id),  # Convert UUID to string
                title=task.title,
                description=task.description,
                status="completed" if task.is_completed else "pending",  # Map is_completed to status
                priority=task.priority,
                type=task.recurrence_pattern or "daily",  # Map recurrence_pattern to type
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at,
                user_id=str(task.user_id)  # Convert UUID to string
            )
            for task in tasks
        ]

    @staticmethod
    async def get_tasks_for_user(user_id: str, session: AsyncSession,
                                 status: Optional[str] = None,
                                 limit: int = 100,
                                 offset: int = 0) -> List[TaskResponse]:
        statement = select(Task).where(Task.user_id == user_id)

        # Map status filter to is_completed field
        if status:
            is_completed_filter = (status.lower() == "completed")
            statement = statement.where(Task.is_completed == is_completed_filter)

        statement = statement.offset(offset).limit(limit)

        result = await session.execute(statement)
        tasks = result.scalars().all()

        return [
            TaskResponse(
                id=str(task.id),  # Convert UUID to string
                title=task.title,
                description=task.description,
                status="completed" if task.is_completed else "pending",  # Map is_completed to status
                priority=task.priority,
                type=task.recurrence_pattern or "daily",  # Map recurrence_pattern to type
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at,
                user_id=str(task.user_id)  # Convert UUID to string
            )
            for task in tasks
        ]

    @staticmethod
    async def update_task_public(task_id: str, task_update: TaskUpdate, session: AsyncSession) -> Optional[TaskResponse]:
        statement = select(Task).where(Task.id == task_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update only provided fields:
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.status is not None:
            task.completed = (task_update.status.lower() == "completed")

        task.updated_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(task)

        # Return response with status mapping:
        # DB 'completed' -> API 'status' (convert boolean to "completed"/"pending")
        status = "completed" if task.completed else "pending"

        return TaskResponse(
            id=str(task.id),  # Convert to string
            title=task.title,
            description=task.description,
            status=status,
            priority="medium",  # Default priority since not in DB model
            type="daily",      # Default type since not in DB model
            due_date=None,     # Default due_date since not in DB model
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=str(task.user_id)  # Convert to string
        )

    @staticmethod
    async def update_task(task_id: str, task_update: TaskUpdate, user_id: str, session: AsyncSession) -> Optional[TaskResponse]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update only provided fields:
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.status is not None:
            task.completed = (task_update.status.lower() == "completed")

        task.updated_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(task)

        # Return response with status mapping:
        # DB 'completed' -> API 'status' (convert boolean to "completed"/"pending")
        status = "completed" if task.completed else "pending"

        return TaskResponse(
            id=str(task.id),  # Convert to string
            title=task.title,
            description=task.description,
            status=status,
            priority="medium",  # Default priority since not in DB model
            type="daily",      # Default type since not in DB model
            due_date=None,     # Default due_date since not in DB model
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=str(task.user_id)  # Convert to string
        )

    @staticmethod
    async def toggle_task_completion_public(task_id: str, session: AsyncSession) -> Optional[TaskResponse]:
        statement = select(Task).where(Task.id == task_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Toggle completion status (is_completed field in database)
        task.is_completed = not task.is_completed
        task.updated_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(task)

        # Return response with field mapping:
        # DB 'is_completed' -> API 'status' (convert boolean to "completed"/"pending")
        # DB 'recurrence_pattern' -> API 'type'
        status = "completed" if task.is_completed else "pending"
        task_type = task.recurrence_pattern or "daily"

        return TaskResponse(
            id=str(task.id),  # Convert UUID to string
            title=task.title,
            description=task.description,
            status=status,
            priority=task.priority,
            type=task_type,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=str(task.user_id)  # Convert UUID to string
        )

    @staticmethod
    async def delete_task_public(task_id: str, session: AsyncSession) -> bool:
        statement = select(Task).where(Task.id == task_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return False

        await session.delete(task)
        await session.commit()
        return True

    @staticmethod
    async def delete_task(task_id: str, user_id: str, session: AsyncSession) -> bool:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return False

        await session.delete(task)
        await session.commit()
        return True

    @staticmethod
    async def toggle_task_completion(task_id: str, user_id: str, session: AsyncSession) -> Optional[TaskResponse]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Toggle completion status (is_completed field in database)
        task.is_completed = not task.is_completed
        task.updated_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(task)

        # Return response with field mapping:
        # DB 'is_completed' -> API 'status' (convert boolean to "completed"/"pending")
        # DB 'recurrence_pattern' -> API 'type'
        status = "completed" if task.is_completed else "pending"
        task_type = task.recurrence_pattern or "daily"

        return TaskResponse(
            id=str(task.id),  # Convert UUID to string
            title=task.title,
            description=task.description,
            status=status,
            priority=task.priority,
            type=task_type,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=str(task.user_id)  # Convert UUID to string
        )

    @staticmethod
    async def get_filtered_tasks(
        session: AsyncSession,
        user_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[TaskResponse], int]:
        """
        Get tasks with filtering options (status, priority, tags, due date range, search) and return total count
        Includes optimization for large datasets with proper indexing and efficient querying
        """
        # Base query with user isolation
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters if provided
        if status:
            is_completed_filter = (status.lower() == "completed")
            query = query.where(Task.completed == is_completed_filter)

        if priority:
            query = query.where(Task.priority == priority.lower())

        if tags:
            # Filter by tags - assuming tags is stored as a JSON array
            for tag in tags:
                query = query.where(Task.tags.op('?')(tag))  # Using PostgreSQL's JSON contains operator

        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)

        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)

        if search:
            # Use full-text search if available, otherwise use ilike
            query = query.where(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%") if Task.description is not None else False
                )
            )

        # Apply sorting
        if sort_by == "priority":
            # Sort by priority with high > medium > low
            priority_order = func.CASE(
                (Task.priority == 'high', 1),
                (Task.priority == 'medium', 2),
                (Task.priority == 'low', 3),
                else_=4
            )
            if sort_order.lower() == "asc":
                query = query.order_by(priority_order.asc(), Task.created_at.desc())
            else:
                query = query.order_by(priority_order.asc(), Task.created_at.desc())
        elif sort_by == "due_date":
            if sort_order.lower() == "asc":
                query = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())
            else:
                query = query.order_by(Task.due_date.desc().nullslast(), Task.created_at.desc())
        elif sort_by == "title":
            if sort_order.lower() == "asc":
                query = query.order_by(Task.title.asc(), Task.created_at.desc())
            else:
                query = query.order_by(Task.title.desc(), Task.created_at.desc())
        else:  # Default to created_at
            if sort_order.lower() == "asc":
                query = query.order_by(Task.created_at.asc())
            else:
                query = query.order_by(Task.created_at.desc())

        # Count total records matching filters (before pagination)
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total_count = total_result.scalar_one()

        # Apply pagination
        paginated_query = query.offset(offset).limit(limit)

        result = await session.execute(paginated_query)
        tasks = result.scalars().all()

        task_responses = [
            TaskResponse(
                id=str(task.id),  # Convert UUID to string
                title=task.title,
                description=task.description,
                status="completed" if task.completed else "pending",  # Map is_completed to status
                priority=task.priority,
                type=task.recurrence_pattern or "daily",  # Map recurrence_pattern to type
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at,
                user_id=str(task.user_id)  # Convert UUID to string
            )
            for task in tasks
        ]

        return task_responses, total_count

    @staticmethod
    async def search_tasks(query: str, session: AsyncSession) -> List[TaskResponse]:
        """
        Search tasks by title or description
        """
        # Create a case-insensitive search query for both title and description
        search_query = select(Task).where(
            or_(
                Task.title.ilike(f"%{query}%"),
                Task.description.ilike(f"%{query}%") if Task.description is not None else False
            )
        )

        result = await session.execute(search_query)
        tasks = result.scalars().all()

        return [
            TaskResponse(
                id=str(task.id),  # Convert UUID to string
                title=task.title,
                description=task.description,
                status="completed" if task.is_completed else "pending",  # Map is_completed to status
                priority=task.priority,
                type=task.recurrence_pattern or "daily",  # Map recurrence_pattern to type
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at,
                user_id=str(task.user_id)  # Convert UUID to string
            )
            for task in tasks
        ]