# Implementation Tasks: Backend Todo API

## Feature: Backend Todo API Implementation

**Overview**: Implementation of a secure, RESTful API backend for the Todo application using Python FastAPI, SQLModel for ORM, and Neon Serverless PostgreSQL for storage. The backend will handle multi-user data isolation via JWT authentication from Better Auth, integrating with frontend API calls.

## Phase 1: Setup

**Goal**: Initialize the project with proper structure and configuration.

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 Set up requirements.txt with dependencies in backend/requirements.txt
- [x] T003 Create root .env and .env.example files with authentication and database variables
- [x] T004 Configure database connection in backend/db.py using asyncpg and SQLModel
- [x] T005 Create backend/CLAUDE.md with development guidelines
- [x] T006 Initialize main.py with FastAPI app setup and basic configuration

## Phase 2: Foundational

**Goal**: Implement foundational components and services that support all user stories.

- [x] T007 [P] Implement User and Task models in backend/models.py using SQLModel
- [x] T008 [P] Create Pydantic schemas in backend/schemas.py for requests/responses
- [x] T009 Implement JWT authentication middleware in backend/auth.py using PyJWT
- [x] T010 [P] Create utility functions in backend/utils.py for recurrence logic
- [x] T011 [P] Set up rate limiting in backend/utils.py using slowapi

## Phase 3: [US1] User Authentication & Authorization

**Goal**: Enable the backend to verify JWT on all requests and filter data by authenticated user.

**User Story**: As the backend, I verify JWT on all requests and filter data by authenticated user.

**Independent Test Criteria**:
- JWT tokens from Authorization header are properly verified using BETTER_AUTH_SECRET
- User_id from JWT payload is validated against URL parameter
- HTTP 401 is returned for invalid/missing tokens
- Authentication is applied to all /api/{user_id}/* routes
- Users can only access their own data (user isolation enforced)

**Implementation Tasks**:

- [x] T012 [US1] Implement JWT token verification function in backend/auth.py
- [x] T013 [US1] Create current_user dependency with token validation in backend/auth.py
- [x] T014 [US1] Implement user_id validation against URL parameter in backend/auth.py
- [x] T015 [US1] Create middleware to apply authentication to all routes in backend/auth.py
- [ ] T016 [US1] Test authentication flow with valid and invalid JWT tokens

## Phase 4: [US2] Task CRUD Operations

**Goal**: Enable the backend to handle task creation, retrieval, updates, deletions, and status toggles with validation.

**User Story**: As the backend, I handle task creation, retrieval, updates, deletions, and status toggles with validation.

**Independent Test Criteria**:
- Users can create tasks with title (required, 1-100 chars), description (≤5000 chars), priority, tags, due_date, recurrence
- Users can retrieve all their tasks with optional filtering and sorting
- Users can update task properties with partial updates allowed
- Users can delete tasks permanently (hard delete)
- Users can toggle task completion status

**Implementation Tasks**:

- [x] T017 [P] [US2] Implement task creation function in backend/crud/tasks.py
- [x] T018 [P] [US2] Implement task retrieval function with filtering in backend/crud/tasks.py
- [x] T019 [P] [US2] Implement task update function with partial updates in backend/crud/tasks.py
- [x] T020 [P] [US2] Implement task deletion function in backend/crud/tasks.py
- [x] T021 [P] [US2] Implement task completion toggle function in backend/crud/tasks.py
- [x] T022 [P] [US2] Create task endpoints in backend/routes/tasks.py for CRUD operations
- [x] T023 [US2] Connect task routes to main application in backend/main.py
- [ ] T024 [US2] Test complete task CRUD workflow with validation

## Phase 5: [US3] Task Properties & Features

**Goal**: Enable the backend to support priorities, tags, due dates, and recurrence patterns.

**User Story**: As the backend, I support priorities, tags, due dates, search/filter/sort queries.

**Independent Test Criteria**:
- System supports priority levels: high, medium, low
- System supports tagging with multiple tags per task
- System supports due dates stored in UTC and converted to user's local time for display
- System supports recurrence patterns: none, daily, weekly
- System maintains created_at and updated_at timestamps

**Implementation Tasks**:

- [x] T025 [P] [US3] Enhance Task model with priority, tags, due_date, recurrence fields in backend/models.py
- [x] T026 [P] [US3] Update Pydantic schemas to include new task properties in backend/schemas.py
- [x] T027 [US3] Implement timezone handling for due dates in backend/utils.py
- [x] T028 [US3] Add timestamp management to Task model in backend/models.py
- [ ] T029 [US3] Test task property creation and updates with validation

## Phase 6: [US4] Search, Filter & Sort

**Goal**: Enable the backend to allow searching, filtering, and sorting of tasks.

**User Story**: As the backend, I support priorities, tags, due dates, search/filter/sort queries.

**Independent Test Criteria**:
- System allows searching by keyword across title and description
- System allows filtering by status (all, pending, completed)
- System allows filtering by priority levels
- System allows date range filtering (from/to specific dates)
- System allows sorting by due_date, priority, or title in ascending/descending order

**Implementation Tasks**:

- [x] T030 [P] [US4] Enhance task retrieval function with search capability in backend/crud/tasks.py
- [x] T031 [P] [US4] Implement status filtering in task retrieval function in backend/crud/tasks.py
- [x] T032 [P] [US4] Implement priority filtering in task retrieval function in backend/crud/tasks.py
- [x] T033 [P] [US4] Implement date range filtering in task retrieval function in backend/crud/tasks.py
- [x] T034 [P] [US4] Implement sorting functionality in task retrieval function in backend/crud/tasks.py
- [x] T035 [US4] Update GET /tasks endpoint to support query parameters in backend/routes/tasks.py
- [ ] T036 [US4] Test search, filter and sort functionality comprehensively

## Phase 7: [US5] Recurring Tasks

**Goal**: Enable the backend to manage recurring tasks (auto-rescheduling logic).

**User Story**: As the backend, I manage recurring tasks (auto-rescheduling logic) and store reminders for frontend triggering.

**Independent Test Criteria**:
- System creates new task instances when recurring tasks are marked complete
- System calculates next due date based on recurrence pattern (daily: +1 day, weekly: +7 days)
- System creates recurring tasks with completed=False status
- System handles recurrence asynchronously to avoid blocking requests
- System creates only the next instance when current task is completed (on-demand creation)

**Implementation Tasks**:

- [x] T037 [P] [US5] Implement recurrence calculation functions in backend/utils.py
- [x] T038 [P] [US5] Update task completion toggle to handle recurrence logic in backend/crud/tasks.py
- [x] T039 [P] [US5] Implement async task creation for recurrence in backend/crud/tasks.py
- [ ] T040 [US5] Test recurring task functionality with daily and weekly patterns
- [ ] T41 [US5] Test recurrence edge cases and error handling

## Phase 8: [US6] Data Isolation & Security

**Goal**: Ensure the backend enforces proper data isolation between users.

**User Story**: As the backend, I verify JWT on all requests and filter data by authenticated user.

**Independent Test Criteria**:
- System filters all queries by user_id to prevent cross-user access
- System validates that requested resources belong to authenticated user
- System returns HTTP 404 for resources belonging to other users
- All authenticated endpoints properly validate JWT tokens
- Rate limiting (100 requests per IP per hour) prevents abuse

**Implementation Tasks**:

- [x] T042 [P] [US6] Enhance all CRUD functions to filter by user_id in backend/crud/tasks.py
- [x] T043 [P] [US6] Implement resource ownership validation in backend/crud/tasks.py
- [x] T044 [P] [US6] Add rate limiting to task endpoints in backend/routes/tasks.py
- [ ] T045 [US6] Test data isolation between different users
- [ ] T046 [US6] Test rate limiting functionality

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Enhance the application with error handling, validation, and performance optimizations.

- [x] T047 Implement comprehensive error handling with proper HTTP status codes
- [x] T048 Add input validation to all endpoints to prevent injection attacks
- [x] T049 Create database indexes for efficient querying (user_id, completed, due_date, priority)
- [x] T050 Optimize database queries for performance
- [x] T051 Add logging for audit trails and debugging
- [ ] T052 Conduct final acceptance testing against all user stories
- [x] T053 Document API endpoints with examples

## Dependencies

- US1 (Authentication & Authorization) must be completed before US2, US3, US4, US5, and US6
- US2 (Task CRUD Operations) is foundational for US3, US4, US5, and US6
- US3 (Task Properties) enhances US2 functionality
- US4 (Search & Filter) builds upon US2 and US3
- US5 (Recurring Tasks) depends on US2 and US3 for task creation
- US6 (Data Isolation) applies to all other user stories

## Parallel Execution Examples

- **Authentication Components** (US1): JWT verification, current_user dependency, middleware can be developed in parallel
- **CRUD Functions** (US2): create_task, get_tasks, update_task, delete_task, toggle_completion can be developed in parallel
- **Filter Components** (US4): Status filter, priority filter, date filter can be developed in parallel
- **Utility Functions** (US3, US5): Timezone handling, recurrence logic, timestamp management can be developed in parallel

## Implementation Strategy

1. **MVP Scope**: Complete US1 (Authentication) and US2 (Task CRUD Operations) for basic functionality
2. **Incremental Delivery**: Add task properties (US3), search/filtering (US4), and recurrence (US5) in subsequent releases
3. **Quality Assurance**: Each user story should be independently testable before moving to the next
4. **Performance**: Optimize for dashboard with up to 1000+ tasks per user, with pagination planned for future scalability