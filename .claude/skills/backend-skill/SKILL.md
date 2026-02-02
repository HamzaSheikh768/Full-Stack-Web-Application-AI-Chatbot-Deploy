---
name: generating-backend-routes
description: Generates backend routes for web applications, handles HTTP requests and responses, and manages database connections. Use this skill when users request assistance with creating or modifying server-side endpoints, integrating data persistence, or building RESTful APIs in frameworks like Express.js, Flask, or Django.
---

# Generating Backend Routes

This skill guides Claude in creating backend code for routes, request/response handling, and database integration. Focus on common frameworks (e.g., Node.js/Express with MongoDB, Python/Flask with SQLAlchemy). Assume user specifies the tech stack; default to Node.js/Express/MongoDB if unspecified.

## Workflow

1. **Gather Requirements**
   - Ask for: Framework/language (e.g., Node.js, Python), DB type (e.g., MongoDB, PostgreSQL), route details (method, path, actions), auth needs, error handling.
   - Checklist:
     - [ ] Route path (e.g., /users)
     - [ ] HTTP methods (GET, POST, etc.)
     - [ ] Request params/body/query
     - [ ] Response format (JSON, status codes)
     - [ ] DB operations (CRUD)
     - [ ] Validation/sanitization
     - [ ] Edge cases (e.g., not found, conflicts)

2. **Plan Structure**
   - Outline file structure: app.js/server.py (entry), routes/users.js (modular), models/user.js (schema).
   - Ensure modularity: Separate concerns (routes, controllers, models).

3. **Generate Code**
   - Start with setup: Install deps (e.g., express, mongoose).
   - Connect DB: Use async connection with error handling.
   - Define routes: Use router middleware.
   - Handle req/res: Parse body, send JSON, set headers.
   - Integrate DB: Query/insert/update/delete with try-catch.
   - Add validation: Use libraries like Joi or Pydantic.

4. **Validate & Test**
   - Suggest unit tests (e.g., Jest, pytest).
   - Error handling: Custom errors, logging.
   - Iterate: Ask user for feedback, refine.

## Output Format

Provide code in fenced blocks with file names. Explain key sections briefly.

Example:

**app.js**

```javascript
const express = require('express');
const mongoose = require('mongoose');
const app = express();

mongoose.connect('mongodb://localhost/db', { useNewUrlParser: true })
  .then(() => console.log('DB connected'))
  .catch(err => console.error('DB connection error:', err));

app.use(express.json());
app.use('/api/users', require('./routes/users'));

app.listen(3000, () => console.log('Server running'));
Examples
Input: "Create a GET route for /users that fetches all users from MongoDB."
Output:

Connect DB in app.js (as above).
models/user.js: Define schema.
routes/users.js:

JavaScriptconst express = require('express');
const router = express.Router();
const User = require('../models/user');

router.get('/', async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;