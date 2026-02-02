# Data Model for Todo App

## User Entity
- **id**: string (primary key, unique identifier)
- **name**: string (user's display name)
- **email**: string (unique, valid email format)
- **themePreference**: 'dark'|'light' (default: 'dark')
- **createdAt**: timestamp (automatically set on creation)
- **updatedAt**: timestamp (automatically updated on changes)

## Task Entity
- **id**: string (primary key, unique identifier)
- **userId**: string (foreign key to User.id, establishes ownership)
- **title**: string (non-empty, max 200 characters)
- **description**: string (optional, max 1000 characters)
- **completed**: boolean (default: false)
- **priority**: 'high'|'medium'|'low' (default: 'medium')
- **dueDate**: timestamp (optional)
- **createdAt**: timestamp (automatically set on creation)
- **updatedAt**: timestamp (automatically updated on changes)

## Conversation Entity
- **id**: string (primary key, unique identifier)
- **userId**: string (foreign key to User.id, establishes ownership)
- **title**: string (auto-generated from first message or user-defined)
- **createdAt**: timestamp (automatically set on creation)
- **updatedAt**: timestamp (automatically updated on changes)

## Message Entity
- **id**: string (primary key, unique identifier)
- **conversationId**: string (foreign key to Conversation.id)
- **userId**: string (foreign key to User.id, identifies sender)
- **role**: 'user'|'assistant' (identifies message source)
- **content**: string (non-empty message content)
- **createdAt**: timestamp (automatically set on creation)

## Relationships
- User (1) ←→ (Many) Task (one-to-many: user has many tasks)
- User (1) ←→ (Many) Conversation (one-to-many: user has many conversations)
- Conversation (1) ←→ (Many) Message (one-to-many: conversation has many messages)

## Validation Rules
- Task.title must be 1-200 characters
- Task.description must be 0-1000 characters if provided
- Priority must be one of 'high', 'medium', or 'low'
- Email must follow standard email format
- Completed status can only be boolean
- User can only access their own tasks, conversations, and messages

## State Transitions
- Task: pending → completed (when marked as complete)
- Task: completed → pending (when marked as incomplete)
- User: light-theme → dark-theme (when theme preference changes)
- User: dark-theme → light-theme (when theme preference changes)