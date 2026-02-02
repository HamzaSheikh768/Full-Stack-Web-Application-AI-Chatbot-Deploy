# Claude Code Instructions: Backend Todo API

## Project Context
You are working on the backend implementation of a Todo application. This is part of Phase II of the Full-Stack Web Application project, focusing exclusively on the backend using Python FastAPI, SQLModel, and Neon Serverless PostgreSQL. The backend serves the frontend application by providing secure, authenticated API endpoints for task management.

## Architecture Overview
- **Framework**: Python FastAPI with async support
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification using PyJWT (integrates with Better Auth)
- **API Style**: RESTful endpoints with consistent response format
- **Rate Limiting**: Implemented with slowapi

## Folder Structure
```
backend
├── main.py                 # FastAPI app entry point, middleware, lifespan events
├── models.py               # SQLModel database models (User, Task)
├── schemas.py              # Pydantic schemas for request/response validation
├── crud/                   # Database operations layer
│   └── tasks.py            # Task-specific CRUD functions
├── routes/                 # API route definitions
│   └── tasks.py            # Task endpoints with authentication
├── db.py                   # Database engine and session setup
├── auth.py                 # JWT middleware and current_user dependency
├── utils.py                # Utility functions (recurrence logic, etc.)
├── requirements.txt        # Python dependencies
├── CLAUDE.md               # Agent instructions (this file)
└── .env                    # Environment variables (not committed)
```

## API Contract
Base URL: `/api/{user_id}/`
All endpoints require JWT authentication in Authorization header: `Authorization: Bearer {token}`

Endpoints:
- `GET /tasks` - Get all user tasks with filtering/sorting
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `PATCH /tasks/{id}/complete` - Toggle completion status

## Authentication Flow
1. JWT token obtained from Better Auth (frontend)
2. Token sent in Authorization header to backend
3. JWT verified using BETTER_AUTH_SECRET
4. User ID extracted from token and compared to URL parameter
5. Request proceeds if user IDs match, otherwise returns 403

## Data Model
### Task Entity
- id: int (PK)
- user_id: str (FK to User, required)
- title: str (required, 1-100 chars)
- description: str (optional, max 5000 chars)
- completed: bool (default False)
- priority: str (enum: 'high', 'medium', 'low', optional)
- tags: List[str] (array of strings, optional)
- due_date: datetime (optional, stored in UTC)
- recurrence: str (enum: 'none', 'daily', 'weekly', default 'none')
- created_at: datetime (auto-set)
- updated_at: datetime (auto-update)

## Development Guidelines
- Use Pydantic for request/response validation
- Use SQLModel for database models and queries
- Implement proper error handling with HTTPException
- Follow FastAPI best practices for dependency injection
- Use async/await for database operations
- Implement proper logging
- Ensure user data isolation (user A cannot access user B's data)

## Security Measures
- JWT token verification on all endpoints
- User ID validation against token and URL
- Input validation to prevent injection attacks
- Rate limiting (100 requests/IP/hour)
- Timezone handling (store in UTC)

## Quality Standards
- Type safety with Pydantic and SQLModel
- Comprehensive error handling
- Proper HTTP status codes
- Consistent response format
- Input validation and sanitization
- Async operations for performance

## Reference Documents
When implementing features, refer to these documents:
- Feature specification: `specs/1-backend-todo-api/spec.md`
- Implementation plan: `specs/1-backend-todo-api/plan.md`
- Data model: `specs/1-backend-todo-api/data-model.md`
- API contracts: `specs/1-backend-todo-api/contracts/api-contracts.md`
- Quickstart guide: `specs/1-backend-todo-api/quickstart.md`

## Development Workflow
1. Read the relevant specification documents before starting implementation
2. Create or update models following SQLModel best practices
3. Define Pydantic schemas for request/response validation
4. Implement CRUD operations in the appropriate files
5. Create API endpoints with proper authentication
6. Add error handling and validation
7. Test endpoints using the interactive documentation