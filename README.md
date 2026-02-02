# TASKAPP - Professional Full-Stack Todo Application with AI Integration

A professional full-stack todo application with Next.js frontend featuring public access without authentication, local storage persistence, dark-first theme with blue accents, AI-powered task management, and comprehensive task management features.

## Features

- 🚀 Next.js 16+ with App Router for modern web development
- 🔓 Public access - no login required to use the application
- 💾 Local storage persistence for tasks and preferences
- 🎨 Dark-first theme with #000000 background, #2563EB blue accents, and #FFFFFF white text
- 🌙 Smooth dark/light theme switching with next-themes
- 📱 Responsive design for all device sizes
- ♿ WCAG 2.1 AA accessibility compliant
- 🔁 Recurring tasks with daily/weekly patterns
- 🏷️ Tag-based task categorization
- 📊 Task filtering, sorting, and search capabilities
- ✨ Smooth animations and loading states

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS, next-themes
- **State Management**: Zustand with persistence
- **Animations**: Framer Motion
- **Drag & Drop**: dnd-kit
- **Styling**: Tailwind CSS with custom dark-first theme

## Prerequisites

- Node.js v20+
- Git

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   # Frontend
   cd frontend
   npm install
   ```
3. Run the application:
   ```bash
   # Frontend
   cd frontend
   npm run dev
   ```

## Project Structure

```
monorepo root
├── .env                          # Environment variables
├── .env.example                  # Example environment variables
├── frontend/                     # Next.js frontend application
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   ├── lib/                      # Utilities and store
│   ├── styles/                   # Global styles
│   └── ...
├── backend/                      # FastAPI backend with AI Chatbot
│   ├── src/                      # Source code
│   │   ├── main.py               # Application entry point
│   │   ├── api/                  # API route definitions
│   │   ├── models/               # SQLModel database models
│   │   ├── mcp/                  # Model Context Protocol tools
│   │   └── agent/                # AI Agent implementation
│   └── ...
```

## AI Chatbot API

The backend includes an AI-powered chatbot that allows users to manage tasks through natural language.

### Chat API Endpoint

- **Endpoint**: `POST /api/{user_id}/chat`
- **Description**: Send a message to the AI assistant and receive a response
- **Headers**:
  - `Content-Type: application/json`
  - Authentication cookie (Better Auth session)
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "number (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "number",
    "response": "string",
    "tool_calls": "array"
  }
  ```

### Supported Commands

The AI assistant can handle various task management commands:

- **Add tasks**: "Add a task to buy groceries", "Create a task to call mom"
- **List tasks**: "Show my tasks", "What do I have to do?", "Show completed tasks"
- **Complete tasks**: "Mark task 1 as complete", "Finish the shopping task"
- **Delete tasks**: "Delete task 1", "Remove the meeting task"
- **Update tasks**: "Change task 1 to 'Call dad'", "Update the grocery task description"

### Environment Variables

Make sure to set the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key for AI processing
- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Secret for authentication