---
name: designing-database-schemas
description: Designs relational database schemas, creates table definitions, and generates migration scripts. Use this skill when users need help with database structure planning, SQL table creation, or versioned schema changes in frameworks like SQLAlchemy, Rails, or raw SQL.
---

# Designing Database Schemas

This skill guides Claude in assisting users with database schema design, table creation, and migrations. Focus on relational databases (e.g., PostgreSQL, MySQL) unless specified otherwise. Assume Claude knows SQL basics; provide concise, actionable steps.

## Core Principles
- Normalize data to 3NF unless performance requires denormalization.
- Use consistent naming: snake_case for columns/tables, descriptive names.
- Include primary keys (id SERIAL PRIMARY KEY), timestamps (created_at, updated_at), indexes for frequent queries.
- Validate user requirements for constraints (UNIQUE, NOT NULL, FOREIGN KEY).
- Handle errors: Suggest fixes for invalid designs (e.g., missing keys).
- Progressive disclosure: Start with high-level schema, drill down on request.

## Workflow: Schema Design
1. **Gather Requirements**: Ask for entities, relationships (one-to-many, many-to-many), attributes, constraints.
2. **Model Entities**: List tables with columns, types (e.g., VARCHAR(255), INTEGER).
3. **Define Relationships**: Add foreign keys, join tables for many-to-many.
4. **Add Indexes/Constraints**: Recommend based on usage (e.g., INDEX on email for users).
5. **Output Schema**: Use SQL DDL format.
6. **Validate**: Check for redundancy, normalization issues; loop back if needed.

Checklist:
- All tables have primary key?
- Foreign keys reference valid tables?
- Data types match expected values (e.g., DATE for dates)?
- Constraints prevent invalid data?

## Workflow: Table Creation
1. **Parse Request**: Identify table name, columns, types from user input.
2. **Generate SQL**: Use CREATE TABLE statement.
3. **Include Options**: Add IF NOT EXISTS, defaults, constraints.
4. **Test Mentally**: Simulate potential issues (e.g., type mismatches).
5. **Output**: Provide full SQL, explain alterations if existing table.

## Workflow: Migrations
1. **Identify Framework**: Detect if SQLAlchemy, Rails, Django, or raw SQL.
2. **Version Changes**: From current schema to new (add/alter/drop columns/tables).
3. **Generate Script**: Use framework syntax (e.g., Alembic for SQLAlchemy).
4. **Up/Down Methods**: Include reversible changes.
5. **Output**: Full migration file content.

## Output Templates

### Schema Diagram (Text-based)
Tables:

users: id (PK), email (UNIQUE), created_at
posts: id (PK), user_id (FK users.id), title, content
Relationships:
users 1:N posts

text### SQL DDL
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    content TEXT
);
Migration Example (Raw SQL)
SQL-- Up
ALTER TABLE users ADD COLUMN password_hash VARCHAR(255);

-- Down
ALTER TABLE users DROP COLUMN password_hash;
Migration Example (SQLAlchemy/Alembic)
Pythonfrom alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('password_hash', sa.String(length=255)))

def downgrade():
    op.drop_column('users', 'password_hash')
Examples
Input: "Design a schema for a blog with users and posts."
Output:
[Use schema diagram template]
[Follow with SQL DDL]
Input: "Create a migration to add a 'bio' column to users table in Rails."
Output:
Rubyclass AddBioToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :bio, :text
  end
end