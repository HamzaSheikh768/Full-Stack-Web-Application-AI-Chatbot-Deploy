from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from .db import AsyncSessionLocal

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session.
    Used with FastAPI's Depends for automatic session management.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()