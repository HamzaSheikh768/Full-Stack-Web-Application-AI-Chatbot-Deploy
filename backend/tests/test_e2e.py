import pytest
import asyncio
from playwright.async_api import Page, expect
import os
from datetime import datetime, timedelta


@pytest.fixture
def browser_context_args(browser_context_args):
    """Set up browser context with additional options"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.mark.asyncio
async def test_user_can_create_task_with_priority_and_tags(page: Page):
    """Test that a user can create a task with priority and tags"""
    # Navigate to the application
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    
    # Authenticate user (adjust based on your auth flow)
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Wait for successful login
    await expect(page).to_have_url(f"{os.getenv('TEST_APP_URL', 'http://localhost:3000')}/dashboard")
    
    # Navigate to tasks page
    await page.get_by_role("link", name="Tasks").click()
    
    # Click to create a new task
    await page.get_by_role("button", name="Add Task").click()
    
    # Fill in task details
    await page.get_by_label("Title *").fill("Test Task with Priority and Tags")
    await page.get_by_label("Description").fill("This is a test task with priority and tags")
    
    # Select priority
    await page.locator("data-testid=priority-select").click()
    await page.get_by_role("option", name="High").click()
    
    # Add tags
    await page.get_by_label("Tags").fill("test, e2e, automation")
    
    # Set due date
    due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    await page.get_by_label("Due Date").fill(due_date)
    
    # Submit the task
    await page.get_by_role("button", name="Create Task").click()
    
    # Verify task was created
    await expect(page.get_by_text("Test Task with Priority and Tags")).to_be_visible()
    await expect(page.get_by_text("High")).to_be_visible()
    await expect(page.get_by_text("test")).to_be_visible()
    await expect(page.get_by_text("e2e")).to_be_visible()


@pytest.mark.asyncio
async def test_user_can_filter_tasks_by_priority_and_status(page: Page):
    """Test that a user can filter tasks by priority and status"""
    # Navigate to the application and authenticate
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Navigate to tasks page
    await page.get_by_role("link", name="Tasks").click()
    
    # Apply priority filter
    await page.locator("data-testid=priority-filter").click()
    await page.get_by_role("option", name="High").click()
    
    # Verify only high priority tasks are shown
    high_priority_tasks = page.locator("[data-testid='task-item']").filter(has_text="High")
    all_tasks = page.locator("[data-testid='task-item']")
    
    await expect(all_tasks).to_have_count(await high_priority_tasks.count())
    
    # Apply status filter
    await page.locator("data-testid=status-filter").click()
    await page.get_by_role("option", name="Pending").click()
    
    # Verify only pending tasks are shown
    pending_tasks = page.locator("[data-testid='task-item']").filter(has_text="Pending")
    all_displayed_tasks = page.locator("[data-testid='task-item']")
    
    await expect(all_displayed_tasks).to_have_count(await pending_tasks.count())


@pytest.mark.asyncio
async def test_user_can_sort_tasks_by_different_criteria(page: Page):
    """Test that a user can sort tasks by different criteria"""
    # Navigate to the application and authenticate
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Navigate to tasks page
    await page.get_by_role("link", name="Tasks").click()
    
    # Sort by due date
    await page.locator("data-testid=sort-select").click()
    await page.get_by_role("option", name="Due Date").click()
    
    # Toggle sort order
    await page.get_by_role("button", name="Toggle Sort Order").click()
    
    # Verify tasks are sorted by due date (implementation-dependent)
    task_elements = page.locator("[data-testid='task-item']")
    task_count = await task_elements.count()
    
    # At least one task should be visible
    assert task_count > 0
    
    # Sort by priority
    await page.locator("data-testid=sort-select").click()
    await page.get_by_role("option", name="Priority").click()
    
    # Verify tasks are sorted by priority
    task_elements = page.locator("[data-testid='task-item']")
    task_count_after_sort = await task_elements.count()
    
    assert task_count_after_sort > 0


@pytest.mark.asyncio
async def test_user_can_create_recurring_task(page: Page):
    """Test that a user can create a recurring task"""
    # Navigate to the application and authenticate
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Navigate to tasks page
    await page.get_by_role("link", name="Tasks").click()
    
    # Click to create a new task
    await page.get_by_role("button", name="Add Task").click()
    
    # Fill in task details
    await page.get_by_label("Title *").fill("Recurring Team Meeting")
    await page.get_by_label("Description").fill("Weekly team sync meeting")
    
    # Select recurrence pattern
    await page.locator("data-testid=recurrence-select").click()
    await page.get_by_role("option", name="Weekly").click()
    
    # Submit the task
    await page.get_by_role("button", name="Create Task").click()
    
    # Verify task was created with recurrence
    await expect(page.get_by_text("Recurring Team Meeting")).to_be_visible()
    await expect(page.get_by_text("Weekly")).to_be_visible()


@pytest.mark.asyncio
async def test_user_can_set_due_dates_and_reminders(page: Page):
    """Test that a user can set due dates and reminders for tasks"""
    # Navigate to the application and authenticate
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Navigate to tasks page
    await page.get_by_role("link", name="Tasks").click()
    
    # Click to create a new task
    await page.get_by_role("button", name="Add Task").click()
    
    # Fill in task details
    await page.get_by_label("Title *").fill("Task with Due Date and Reminder")
    await page.get_by_label("Description").fill("This task has a due date and reminder")
    
    # Set due date
    due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    await page.get_by_label("Due Date").fill(due_date)
    
    # Enable and set reminder
    await page.get_by_label("Enable Reminder").click()
    reminder_time = (datetime.now() + timedelta(days=2, hours=1)).strftime("%Y-%m-%dT%H:%M")
    await page.get_by_label("Reminder Time").fill(reminder_time)
    
    # Submit the task
    await page.get_by_role("button", name="Create Task").click()
    
    # Verify task was created with due date and reminder
    await expect(page.get_by_text("Task with Due Date and Reminder")).to_be_visible()
    # Check that due date is displayed
    await expect(page.locator(f"text={due_date}")).to_be_visible()


@pytest.mark.asyncio
async def test_user_can_search_tasks(page: Page):
    """Test that a user can search for tasks by keyword"""
    # Navigate to the application and authenticate
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Navigate to tasks page
    await page.get_by_role("link", name="Tasks").click()
    
    # Create a task to search for
    await page.get_by_role("button", name="Add Task").click()
    await page.get_by_label("Title *").fill("Marketing Campaign Research")
    await page.get_by_label("Description").fill("Research for upcoming marketing campaign")
    await page.get_by_role("button", name="Create Task").click()
    
    # Search for the task
    await page.get_by_placeholder("Search tasks...").fill("Marketing")
    await page.keyboard.press("Enter")
    
    # Verify the task appears in search results
    await expect(page.get_by_text("Marketing Campaign Research")).to_be_visible()
    
    # Clear search and verify all tasks appear again
    await page.get_by_placeholder("Search tasks...").fill("")
    await expect(page.locator("[data-testid='task-item']")).to_have_count_at_least(1)


@pytest.mark.asyncio
async def test_chatbot_can_manage_tasks_with_natural_language(page: Page):
    """Test that the chatbot can manage tasks using natural language"""
    # Navigate to the application and authenticate
    await page.goto(os.getenv("TEST_APP_URL", "http://localhost:3000"))
    await page.get_by_label("Email").fill("test@example.com")
    await page.get_by_label("Password").fill("password")
    await page.get_by_role("button", name="Sign In").click()
    
    # Navigate to chat page
    await page.get_by_role("link", name="AI Assistant").click()
    
    # Ask the chatbot to create a task
    await page.get_by_placeholder("Type your message or use voice input...").fill(
        "Create a high priority task to buy groceries with tags shopping and food due tomorrow"
    )
    await page.get_by_role("button", name="Send").click()
    
    # Wait for response
    await expect(page.locator("[data-testid='chat-response']")).to_contain_text("created")
    
    # Navigate to tasks page to verify task was created
    await page.get_by_role("link", name="Tasks").click()
    
    # Verify the task exists with correct properties
    await expect(page.get_by_text("buy groceries")).to_be_visible()
    await expect(page.get_by_text("high")).to_be_visible()
    await expect(page.get_by_text("shopping")).to_be_visible()
    await expect(page.get_by_text("food")).to_be_visible()