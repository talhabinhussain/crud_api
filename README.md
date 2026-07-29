# CRUD API — Route Project

A simple **Task CRUD API** built with **FastAPI** + **SQLModel** + **SQLite**.

Changing the shape of a table felt a bit like rearranging furniture in a room you already lived in: everything still worked, but the whole layout had shifted underneath you. That uneasy feeling is exactly why migrations exist, and you’ll meet them properly in a later week.

---

## Tech Stack

| Layer    | Technology                      |
| -------- | ------------------------------- |
| Web      | FastAPI (with standard extras)  |
| ORM      | SQLModel                        |
| Database | SQLite                          |
| Language | Python 3.13+                    |

---

## Folder Structure

```
crud_api/
├── app/
│   ├── models/
│   │   └── task_model.py       # Pydantic / SQLModel schemas (Task, CreateTask, UpdateTask)
│   ├── repository/
│   │   └── task_repo.py        # Raw database queries (all_task, get_id, insert_task, task_delete, get_stats)
│   ├── routes/
│   │   └── todo_route.py       # HTTP endpoint definitions
│   └── services/
│       └── task_service.py     # Business logic & error handling
|   └── database/
│         └── task_db.py              # Engine, session factory, table creation
├── main.py                     # FastAPI app entry point
├── pyproject.toml              # Dependencies & project metadata
├── task.db                     # SQLite database file (auto-generated)
└── README.md
```

### Architecture Flow

```
Client  →  Route (routes/)  →  Service (services/)  →  Repository (repository/)  →  Database (database/)
```

---

## Database & ORM Decisions

### Why a Database Instead of In-Memory Data?

An in-memory list or dict disappears when the server stops, can't survive crashes, can't be shared across processes, and offers no query language. A database (SQLite) gives persistence, concurrent-safe access, structured queries, and data integrity — without needing a separate server process.

### Database Schema

![Database Schema](/public/db-screenshot.jpg)

> *Screenshot of my database tables with some records and required field.*

### Why an ORM Instead of Raw SQL?

SQLModel provides Pythonic type safety, auto-generated DDL, composable queries (method chaining), and automatic parameter binding — reducing boilerplate and eliminating entire classes of SQL injection and type-mismatch bugs.

### SQLModel Code vs Equivalent Raw SQL

Each function in `app/repositories/task_repo.py` uses SQLModel; here is the equivalent raw SQL:

| Function | SQLModel (task_repo.py) | Equivalent Raw SQL |
|---|---|---|
| `all_task` | `select(Task).where(...).order_by(...)` | `SELECT * FROM task WHERE title LIKE ? AND done = ? ORDER BY title` |
| `get_id` | `session.get(Task, id)` | `SELECT * FROM task WHERE id = ?` |
| `insert_task` | `session.add(task); session.commit()` | `INSERT INTO task (title, done) VALUES (?, ?)` |
| `task_delete` | `session.delete(task); session.commit()` | `DELETE FROM task WHERE id = ?` |
| `get_stats` | `select(func.count(Task.id)).where(...)` | `SELECT COUNT(id) FROM task WHERE done = 1` |

### Why Query Parameters?

Query parameters in `all_task` (`search`, `done`) let the client filter results flexibly without creating a new endpoint per filter combination.

### What Is an Index?

An index is a sorted lookup structure (like a book's index) that lets the database find rows without scanning the entire table — speeding up `WHERE`, `ORDER BY`, and `JOIN` operations.

---

## Endpoints

| Method   | Path              | Description       |
| -------- | ----------------- | ----------------- |
| `GET`    | `/health`         | Health check      |
| `GET`    | `/tasks`          | List all tasks    |
| `GET`    | `/task/{id}`      | Get task by ID    |
| `POST`   | `/task`           | Create a new task |
| `PUT`    | `/task/{id}`      | Update a task     |
| `GET`    | `/stats`          | Task statistics (total, done, open) |
| `DELETE` | `/task/delete/{id}` | Delete a task   |

Total **7 endpoints**.

---

## How to Run

```bash
# Install dependencies
uv sync

# Start the server
uv run uvicorn main:app --reload
```

Server starts at **http://localhost:8000**.  
Swagger docs at **http://localhost:8000/docs**.

---

## Curl Examples with Expected Output

### 1. Health Check

```bash
curl.exe -X GET http://localhost:8000/health
```

```json
{"status":"ok"}
```

### 2. Task Statistics

```bash
curl.exe -X GET http://localhost:8000/stats
```

```json
{"total":3,"done":1,"open":2}
```

### 3. List All Tasks (empty)

```bash
curl.exe -X GET http://localhost:8000/tasks
```

```json
[]
```

### 4. Create a Task

```bash
curl.exe -X POST http://localhost:8000/task ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"coding\",\"done\":false}"
```

```json
"task is created"
```

### 5. List All Tasks (after creation)

```bash
curl.exe -X GET http://localhost:8000/tasks
```

```json
[{"done":false,"id":1,"title":"coding"}]
```

### 6. Get Task by ID

```bash
curl.exe -X GET http://localhost:8000/task/1
```

```json
{"done":false,"id":1,"title":"coding"}
```

### 7. Update a Task

```bash
curl.exe -X PUT http://localhost:8000/task/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"updated coding\",\"done\":true}"
```

```json
"id 1 was added successfully"
```

### 8. Delete a Task

```bash
curl.exe -X DELETE http://localhost:8000/task/delete/1
```

```json
"id 1 is deleted"
```

### 9. Get Task by ID (not found)

```bash
curl.exe -X GET http://localhost:8000/task/999
```

```json
{"detail":"id 999 not found"}
```

---

# AI vs Me — Comparison

The **`crud_api/`** (root) project was written **manually by me**.  
The **`ai-version/`** project was generated **by an AI agent (agentic coding)**.

Both use the same tech stack (FastAPI + SQLModel + SQLite) and implement the same 7 CRUD + health + stats operations. Below is a side-by-side analysis.

| Criteria              | Me (Route)                                             | AI (ai-version)                                          | Better       |
| --------------------- | ------------------------------------------------------- | -------------------------------------------------------- | ------------ |
| **Package init**      | ❌ No `__init__.py` in sub-packages                     | ✅ `__init__.py` in every package                        | AI           |
| **RESTful URLs**      | ❌ `DELETE /task/delete/{id}` (non-standard)            | ✅ `DELETE /task/{id}` (RESTful)                         | AI           |
| **HTTP Status Codes** | ❌ PUT returns 201, DELETE returns 202                  | ✅ PUT → 200, DELETE → 204 (RFC-compliant)              | AI           |
| **Response Body**     | ❌ Create/Update return plain strings                   | ✅ Returns created/updated JSON object                   | AI           |
| **Create logic**      | ❌ Inline in route (duplicated from service)            | ✅ Delegated to `create_task` service function           | AI           |
| **Partial Updates**   | ❌ `UpdateTask` requires all fields                     | ✅ All fields optional — true PATCH semantics            | AI           |
| **Startup Lifecycle** | ❌ Deprecated `@app.on_event("startup")`                | ✅ Modern `lifespan` async context manager               | AI           |
| **Typo**              | ❌ `get_sessin` (missing `o`)                           | ✅ `get_session`                                         | AI           |
| **Dead Code**         | ❌ Unused imports (`Depends`, `HTTPException` in route) | ✅ Clean imports, no dead code                           | AI           |
| **Tests**             | ❌ No tests                                             | ✅ pytest + TestClient with isolated test DB (10 tests)  | AI           |
| **Dev Dependencies**  | ❌ Not configured                                       | ✅ `pytest`, `httpx` in `[project.optional-dependencies]` | AI           |
| **.gitignore**        | ❌ Missing `*.db`, `.pytest_cache/`                     | ✅ Covers `*.db`, `.pytest_cache/`                       | AI           |

## Verdict

> The AI version follows REST best practices, returns proper HTTP status codes and structured JSON, uses modern FastAPI patterns (lifespan, optional fields), includes a comprehensive test suite, and has cleaner package structure — while the manually written route project contains inconsistent status codes, non-RESTful URLs, dead code, a typo, and no tests.
