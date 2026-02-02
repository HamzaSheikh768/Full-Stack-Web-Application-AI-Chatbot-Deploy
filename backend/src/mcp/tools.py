from typing import List, Dict, Any, Optional
from ..models.task import Task
from ..models.conversation import Conversation, Message
from sqlmodel import select
from datetime import datetime, timezone
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Import the handlers that perform the actual DB operations
from .handlers import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)

# Define the tools that will be available to the AI agent
all_tools = [
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
]