# Migration Guide: Advanced Todo Features

## Overview

This guide provides instructions for existing users migrating to the new version of the Todo application with advanced features including priorities, tags, search/filter, sort, recurring tasks, and due dates & reminders.

## What's New

The new version introduces several advanced features:

1. **Task Priorities**: Assign high, medium, or low priority to tasks
2. **Task Tags**: Categorize tasks with customizable tags
3. **Search & Filter**: Quickly find tasks using keywords and filters
4. **Sorting**: Organize tasks by various criteria
5. **Recurring Tasks**: Create tasks that repeat on a schedule
6. **Due Dates & Reminders**: Set deadlines and receive timely notifications

## Migration Process

### Automatic Migration

Most aspects of the migration happen automatically when you log in to the new version:

1. Your existing tasks will be preserved
2. Default priority will be set to "medium" for all existing tasks
3. No tags will be assigned to existing tasks initially
4. No due dates or reminders will be set for existing tasks

### Manual Configuration

After logging in, you may want to:

1. **Review existing tasks** to assign appropriate priorities
2. **Add tags** to categorize your existing tasks
3. **Set due dates** for tasks that have deadlines
4. **Configure recurring tasks** for activities you do regularly

## Updating Your Workflow

### Using Priorities

- Review your current task list and assign priorities
- Focus on high-priority tasks first
- Use priorities to filter your view when needed

### Using Tags

- Create tags for common categories (e.g., "work", "personal", "errands")
- Use tags to group related tasks
- Filter by tags to focus on specific areas

### Taking Advantage of Search

- Use the search bar to quickly find tasks
- Search by keywords in titles or descriptions
- Combine search with filters for more precise results

### Setting Up Recurring Tasks

- Identify tasks you do regularly (weekly meetings, monthly reports, etc.)
- Convert these to recurring tasks to save time
- Set appropriate recurrence patterns

## API Changes

If you're using the API, note these changes:

### New Fields in Task Objects
- `priority`: Task priority level (high, medium, low)
- `tags`: Array of tag strings
- `due_date`: ISO 8601 formatted due date
- `remind_at`: ISO 8601 formatted reminder time
- `is_recurring`: Boolean indicating if task recurs
- `recurrence_pattern`: Object defining recurrence pattern
- `next_due_date`: ISO 8601 formatted next occurrence date

### New API Endpoints
- `/api/users/{user_id}/tasks/search`: Search tasks by keyword
- `/api/users/{user_id}/tasks/filter`: Filter tasks with multiple criteria
- `/api/users/{user_id}/tasks/sort`: Sort tasks by various criteria

### Updated API Endpoints
- `/api/users/{user_id}/tasks` now supports additional query parameters for filtering and sorting

## Mobile App Updates

- Download the latest version from your app store
- Sign in with your existing credentials
- The new features will be available immediately
- Review your task list to take advantage of new capabilities

## Training Resources

### Video Tutorials
- [Getting Started with Priorities and Tags](link)
- [Mastering Search and Filter](link)
- [Setting Up Recurring Tasks](link)
- [Using Due Dates and Reminders](link)

### Interactive Walkthrough
- Access the interactive tutorial from the Help menu
- Practice using new features in a guided environment
- Learn shortcuts and best practices

## Common Questions

### Will my existing tasks be affected?
Your existing tasks will be preserved. New fields will be populated with sensible defaults.

### Do I need to re-enter all my tasks?
No, all your existing tasks will carry over automatically.

### Can I turn off the new features if I don't want to use them?
Yes, all new features are optional. You can continue using the app as before.

### How do I learn to use the new features?
Use the in-app tutorials or consult the user guide for detailed instructions.

## Support During Migration

If you encounter issues during migration:

1. Check the FAQ in the app
2. Use the in-app chat support
3. Email our support team at support@todo-app.com
4. Join our migration support webinar (schedule in app)

## Timeline

- **Week 1**: New version deployed to production
- **Week 2-3**: Active migration period with support available
- **Week 4**: Legacy version support ends
- **Ongoing**: Support for new features continues

## Rollback Information

If critical issues arise, you can temporarily rollback to the previous version by contacting support. However, we recommend moving forward with the new version as the old version will eventually be discontinued.

## Feedback

We welcome your feedback on the new features:
- Use the feedback form in the app
- Participate in our user surveys
- Join our beta testing program for future features

## Next Steps

1. Update to the latest version
2. Explore the new features using the interactive tutorial
3. Gradually incorporate new features into your workflow
4. Provide feedback to help us improve