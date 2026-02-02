---
id: "018"
title: "Improved Chatbot Task Creation Recognition"
stage: "general"
date_iso: "2026-02-01"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "2-ui-ux-design"
user: "user"
command: "sp.implement"
labels: ["bug-fix", "ai-agent", "task-creation", "intent-recognition"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/agent/core.py"
tests_yaml: []
---

# Improved Chatbot Task Creation Recognition

## User Input
```
why this issue resolved chatbot correct answer kyun nh dey rha hai create task 'buy watch'
```

## Response Text
Fixed the issue where the chatbot was not correctly recognizing and processing task creation commands like "create task 'buy watch'". The problem was that the AI model wasn't properly identifying user intents to create tasks.

Changes made:

1. Enhanced the agent instructions in `backend/src/agent/core.py` to be more explicit about recognizing various task creation commands such as 'create task', 'add task', 'make task', 'remember to', 'need to', 'buy', 'get', etc.

2. Added specific instruction to use the add_task function when a user wants to create a task, with appropriate title and optional description.

3. Changed the AI model from "command-r-plus" to "command-r" which is more commonly available via Cohere's API.

These changes should help the AI model better understand when users want to create tasks and properly invoke the add_task function with the correct parameters.

## Outcome
The chatbot should now properly recognize commands like "create task 'buy watch'" and correctly call the add_task function to create the task in the database.

## Evaluation
The fix improves the AI's ability to recognize task creation intents, which should resolve the issue with task creation not working properly.