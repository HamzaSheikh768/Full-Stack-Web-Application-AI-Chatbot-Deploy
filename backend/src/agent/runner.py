import re
from typing import List, Dict, Any
from sqlmodel import select
from ..database.db import SessionLocal
from ..models.conversation import Conversation, Message
from .core import get_agent
import json
from pathlib import Path
import logging


def run_agent_sync(user_id: str, message_text: str, conversation_id: int = None) -> Dict[str, Any]:
    """
    Synchronous agent runner that:
    1. Loads conversation from DB
    2. Runs agent with tools
    3. Saves response to DB
    4. Returns response (stateless - no server memory)
    """
    with SessionLocal() as session:
        # 1. Get or Create Conversation
        if conversation_id:
            conv = session.get(Conversation, conversation_id)
            if not conv or conv.user_id != user_id:
                # If conversation doesn't exist or doesn't belong to user, create new
                conv = Conversation(user_id=user_id)
                session.add(conv)
                session.commit()
        else:
            conv = Conversation(user_id=user_id)
            session.add(conv)
            session.commit()

        # Refresh to get the ID if it was newly created
        session.refresh(conv)
        real_cid = conv.id

        # 2. Persist User Message
        user_msg = Message(
            conversation_id=real_cid,
            role="user",
            content=message_text
        )
        session.add(user_msg)
        session.commit()

        # 3. Load Conversation History
        msgs_query = select(Message).where(
            Message.conversation_id == real_cid
        ).order_by(Message.created_at)
        result = session.execute(msgs_query)
        db_history = result.all()

        # Convert Row objects to proper Message model instances
        # The result.all() returns Row objects where the first element is the Message
        message_objects = [row[0] for row in db_history]
        messages = [{"role": msg.role, "content": msg.content} for msg in message_objects]

        # 4. Run Agent with User-Scoped Tools
        agent_data = get_agent(user_id)
        client = agent_data["client"]
        tools = agent_data["tools"]

        # For Cohere, we don't need to load tool definitions since we're using
        # a different approach than OpenAI's tool calling
        # The tools will be invoked based on intent parsing instead

        # 5. Run Agent (Tool Loop with proper tool calling)
        final_message = "I'm sorry, I encountered an error."
        tool_calls_made = []

        try:
            # Use Cohere's native chat API instead of OpenAI's
            # Cohere doesn't support tool calling in the same way as OpenAI
            # So we'll use generative prompting and parse the response

            # Use Cohere's chat API (more appropriate than generate for conversation)
            # Format the chat history for Cohere
            chat_message = messages[-1]['content'] if messages else "Hello"

            # Get previous messages as preamble/context
            preamble = "You are a helpful and friendly Todo Assistant. You organize tasks for the user with care and attention. Always be conversational and helpful."

            # Prepare chat history
            chat_history = []
            for msg in messages[:-1]:  # All messages except the last one (current)
                role = "USER" if msg['role'] == 'user' else "CHATBOT"
                chat_history.append({"role": role, "message": msg['content']})

            # Call Cohere's chat API
            response = client.chat(
                message=chat_message,
                preamble=preamble,
                chat_history=chat_history,
                temperature=0.7
            )

            # Extract the generated text
            final_message = response.text

            # Parse the response for task-related intents
            # This is our replacement for tool calling functionality
            last_user_message = ""
            for msg in reversed(messages):
                if msg['role'] == 'user':
                    last_user_message = msg['content']
                    break

            # Simple intent detection and extraction
            user_msg_lower = last_user_message.lower()
            response_lower = final_message.lower()

            # Intent: Add/Create Task
            if any(intent_word in user_msg_lower for intent_word in ['add', 'create', 'make', 'new task', 'remember to', 'need to']):
                # Extract task title and potential description using regex patterns
                # Try to extract both title and description from the user's message
                patterns = [
                    # Pattern that captures both title and description
                    r'(?:add|create|make|remember to|need to|buy|get|do|complete|finish)\s+(?:a\s+|an\s+|the\s+|my\s+)?(?:task|to|that|for)\s+(.+?)(?:\.|!|\?|$)',
                    r'(?:add|create|make|remember to|need to|buy|get|do|complete|finish)\s+(.+?)(?:\.|!|\?|$)',
                    r'(?:i want to|i need to|let me)\s+(.+?)(?:\.|!|\?|$)'
                ]

                for pattern in patterns:
                    match = re.search(pattern, last_user_message, re.IGNORECASE)
                    if match:
                        extracted_text = match.group(1).strip().rstrip('.!?')

                        # Try to separate title and description based on common separators
                        # Look for phrases that might indicate a description follows
                        title = extracted_text
                        description = None

                        # Check if there's a separator that indicates a description follows
                        if any(separator in extracted_text.lower() for separator in [' - ', ' – ', ': ', ' -', ' –', ':', 'because', 'since', 'for', 'to']):
                            parts = re.split(r'(?:\s*[-–:]\s*|\s+(?:because|since|for|to)\s+)', extracted_text, 1)
                            if len(parts) > 1:
                                title = parts[0].strip()
                                description = parts[1].strip()

                        # Execute add_task tool manually with both title and description
                        tool_params = {"title": title}
                        if description:
                            tool_params["description"] = description

                        tool_result = _execute_tool_with_user_context_sync(
                            user_id, "add_task", tool_params
                        )

                        tool_calls_made.append({
                            "name": "add_task",
                            "arguments": tool_params,
                            "result": tool_result
                        })

                        if "error" not in tool_result:
                            if description:
                                final_message = f"I've added '{title}' to your task list with description: '{description}'. Is there anything else I can help you with?"
                            else:
                                final_message = f"I've added '{title}' to your task list. Is there anything else I can help you with?"
                        else:
                            final_message = f"I tried to add the task but encountered an error: {tool_result.get('error', 'Unknown error')}"
                        break
                else:
                    # If no specific task could be extracted
                    final_message = f"I understand you want to add a task. {final_message}"

            # Intent: List Tasks
            elif any(intent_word in user_msg_lower for intent_word in ['show', 'list', 'view', 'see', 'my tasks', 'what']):
                if any(show_word in user_msg_lower for show_word in ['all', 'pending', 'incomplete', 'not done']):
                    status_param = "pending"
                elif any(show_word in user_msg_lower for show_word in ['done', 'completed', 'finished']):
                    status_param = "completed"
                else:
                    status_param = "all"

                # Execute list_tasks tool
                tool_result = _execute_tool_with_user_context_sync(
                    user_id, "list_tasks", {"status": status_param}
                )

                tool_calls_made.append({
                    "name": "list_tasks",
                    "arguments": {"status": status_param},
                    "result": tool_result
                })

                if "error" not in tool_result:
                    if tool_result:  # If there are tasks
                        # Create a more compact table with clear separation
                        header_line = "┌──────────────────┬─────────────────────────────────────────────────────────────────────────────┬──────────┐"
                        footer_line = "└──────────────────┴─────────────────────────────────────────────────────────────────────────────┴──────────┘"
                        separator_line = "├──────────────────┼─────────────────────────────────────────────────────────────────────────────┼──────────┤"

                        # Create header row
                        header_row = "│ Task ID          │ Task Title (Description)                                                      │ Status   │"

                        # Start building the table
                        table_lines = [header_line, header_row, separator_line]

                        # Add each task as a row
                        for task in tool_result:
                            task_id = task.get('id', 'N/A')
                            # Convert task_id to string to handle both numeric IDs and UUIDs
                            task_id_str = str(task_id)

                            title = task.get('title', 'Untitled')
                            description = task.get('description', '')  # Get description if available

                            # Combine title and description if description exists
                            if description:
                                display_content = f"{title} - {description}"
                            else:
                                display_content = title

                            status = "Completed" if task.get('completed', False) else "Pending"

                            # Truncate long content for display (more compact than before)
                            display_content = display_content[:70] + "..." if len(display_content) > 70 else display_content

                            # Create a properly aligned table row with more compact formatting
                            table_row = f"│ {task_id_str[:14]:<14} │ {display_content:<69} │ {status:<8} │"
                            table_lines.append(table_row)

                        table_lines.append(footer_line)
                        table_content = "\n".join(table_lines)

                        final_message = f"Here are your {status_param} tasks:\n\n{table_content}\n\nIs there anything else you'd like to do?"
                    else:
                        final_message = f"You don't have any {status_param} tasks right now. Would you like to add one?"
                else:
                    final_message = f"I tried to list your tasks but encountered an error: {tool_result.get('error', 'Unknown error')}"

            # Intent: Complete Task
            elif any(intent_word in user_msg_lower for intent_word in ['complete', 'done', 'finish', 'mark as done']):
                # Look for task ID in the message
                id_match = re.search(r'\b(\d+)\b', last_user_message)
                if id_match:
                    task_id = int(id_match.group(1))

                    # Execute complete_task tool
                    tool_result = _execute_tool_with_user_context_sync(
                        user_id, "complete_task", {"task_id": task_id}
                    )

                    tool_calls_made.append({
                        "name": "complete_task",
                        "arguments": {"task_id": task_id},
                        "result": tool_result
                    })

                    if "error" not in tool_result:
                        final_message = f"I've marked task #{task_id} as completed. Is there anything else I can help with?"
                    else:
                        final_message = f"I tried to complete the task but encountered an error: {tool_result.get('error', 'Unknown error')}"
                else:
                    # If no ID found, list tasks for selection
                    list_result = _execute_tool_with_user_context_sync(
                        user_id, "list_tasks", {"status": "pending"}
                    )
                    if "error" not in list_result and list_result:
                        task_list = "\n".join([f"- #{task.get('id', 'N/A')}: {task.get('title', 'Untitled')}" for task in list_result])
                        final_message = f"I'm not sure which task to complete. Here are your pending tasks:\n{task_list}\n\nPlease specify which task number to complete."
                    else:
                        final_message = "I couldn't find your tasks to complete. Please specify the task number."

            # Intent: Delete Task
            elif any(intent_word in user_msg_lower for intent_word in ['delete', 'remove', 'erase', 'cancel']):
                # Look for task ID in the message
                id_match = re.search(r'\b(\d+)\b', last_user_message)
                if id_match:
                    task_id = int(id_match.group(1))

                    # Execute delete_task tool
                    tool_result = _execute_tool_with_user_context_sync(
                        user_id, "delete_task", {"task_id": task_id}
                    )

                    tool_calls_made.append({
                        "name": "delete_task",
                        "arguments": {"task_id": task_id},
                        "result": tool_result
                    })

                    if "error" not in tool_result:
                        final_message = f"I've deleted task #{task_id}. Is there anything else I can help with?"
                    else:
                        final_message = f"I tried to delete the task but encountered an error: {tool_result.get('error', 'Unknown error')}"
                else:
                    # If no ID found, list tasks for selection
                    list_result = _execute_tool_with_user_context_sync(
                        user_id, "list_tasks", {"status": "all"}
                    )
                    if "error" not in list_result and list_result:
                        task_list = "\n".join([f"- #{task.get('id', 'N/A')}: {task.get('title', 'Untitled')}" for task in list_result])
                        final_message = f"I'm not sure which task to delete. Here are your tasks:\n{task_list}\n\nPlease specify which task number to delete."
                    else:
                        final_message = "I couldn't find your tasks to delete. Please specify the task number."

            # Intent: Update Task
            elif any(intent_word in user_msg_lower for intent_word in ['update', 'change', 'modify', 'edit', 'rename']):
                # Look for task ID and new title in the message
                id_match = re.search(r'\b(\d+)\b', last_user_message)
                # Look for text that might be the new title after words like "to", "as", etc.
                title_match = re.search(r'(?:to|as|into|with)\s+(.+?)(?:\.|!|\?|$)', last_user_message, re.IGNORECASE)

                if id_match and title_match:
                    task_id = int(id_match.group(1))
                    new_title = title_match.group(1).strip()

                    # Execute update_task tool
                    tool_result = _execute_tool_with_user_context_sync(
                        user_id, "update_task", {"task_id": task_id, "title": new_title}
                    )

                    tool_calls_made.append({
                        "name": "update_task",
                        "arguments": {"task_id": task_id, "title": new_title},
                        "result": tool_result
                    })

                    if "error" not in tool_result:
                        final_message = f"I've updated task #{task_id} to '{new_title}'. Is there anything else I can help with?"
                    else:
                        final_message = f"I tried to update the task but encountered an error: {tool_result.get('error', 'Unknown error')}"
                else:
                    final_message = f"I understand you want to update a task. {final_message}"

        except Exception as e:
            # Enhanced error handling with more specific debugging
            error_str = str(e).lower()
            logging.error(f"Cohere API error details: {str(e)}")

            # Check if it's an API key, connection, or HTTP method issue
            if 'api' in error_str or 'key' in error_str or 'authorization' in error_str or '401' in error_str or '403' in error_str:
                logging.error(f"LLM API error (likely configuration issue): {str(e)}")
                final_message = "I'm sorry, I'm currently unable to connect to the AI service. This is likely because the COHERE_API_KEY is invalid or missing. Please make sure your API key is properly configured in the environment variables."
            elif '400' in error_str or 'invalid' in error_str:
                logging.error(f"LLM API error (bad request): {str(e)}")
                final_message = "I'm sorry, there was an issue with the request to the AI service. The configuration might need adjustment."
            elif 'connection' in error_str or 'network' in error_str or 'timeout' in error_str:
                logging.error(f"LLM API error (network/connection): {str(e)}")
                final_message = "I'm sorry, I'm having trouble connecting to the AI service. Please check your internet connection and make sure the API endpoint is accessible."
            else:
                logging.error(f"Agent processing error: {str(e)}")
                final_message = f"I'm sorry, I encountered an error: {str(e)[:200]}..."  # Limit length for safety
        # 6. Persist Assistant Response
        asst_msg = Message(
            conversation_id=real_cid,
            role="assistant",
            content=final_message
        )
        session.add(asst_msg)
        session.commit()

        return {
            "conversation_id": real_cid,
            "response": final_message,
            "tool_calls": tool_calls_made
        }


# Global variable to hold the user_id for the current execution context
# This is a simple way to pass user_id to the execute_tool function
# In a real implementation, we'd use a more sophisticated context mechanism
_current_user_id = None


def execute_tool_sync(function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the appropriate tool based on function name"""
    from ..mcp.handlers import add_task, list_tasks, complete_task, delete_task, update_task

    # Add the current user_id to the function arguments to ensure proper isolation
    # Only add user_id if it's not already in the function_args (to prevent duplication)
    if _current_user_id and 'user_id' not in function_args:
        function_args["user_id"] = _current_user_id

    if function_name == "add_task":
        return add_task(**function_args)
    elif function_name == "list_tasks":
        return list_tasks(**function_args)
    elif function_name == "complete_task":
        return complete_task(**function_args)
    elif function_name == "delete_task":
        return delete_task(**function_args)
    elif function_name == "update_task":
        return update_task(**function_args)
    else:
        return {"error": f"Unknown function: {function_name}"}


def _execute_tool_with_user_context_sync(user_id: str, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tool with proper user context"""
    global _current_user_id
    _current_user_id = user_id

    try:
        result = execute_tool_sync(function_name, function_args)
        return result
    finally:
        # Reset the context after execution
        _current_user_id = None


def execute_tool(function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function to maintain compatibility with existing calls"""
    return execute_tool_sync(function_name, function_args)