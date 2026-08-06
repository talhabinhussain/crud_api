# CRUD API — Route Project

A simple **Task CRUD API** built with **FastAPI** + **SQLModel** + **PostgreSQL** running inside a local **Docker** container.

---

## Project Evolution & Storage History

The persistence layer of this project has evolved through three major iterations:

1. **In-Memory Python List (Initial Implementation):** Simple and fast, but all data was lost every time the server restarted.
2. **SQLite Database (Assignment 2):** Switched to a lightweight, file-based SQL database (`task.db`) using SQLModel. Data persisted across server restarts, but concurrency was limited and database files were tracked locally in the codebase.
3. **PostgreSQL inside Docker (Current Implementation):** Migrated to a robust, production-grade PostgreSQL database isolated inside a Docker container, with data persisting in a Docker Volume.

---

## Tech Stack

| Layer    | Technology                                  |
| -------- | ------------------------------------------- |
| Web      | FastAPI (with standard extras)              |
| ORM      | SQLModel                                    |
| Database | PostgreSQL 17 (local Docker container)      |
| Language | Python 3.13+                                |

---

## Database Architecture

The application no longer uses SQLite as its primary database. The backend now connects to a PostgreSQL database running locally inside a Docker container.

### Component Architecture

```text
                Docker Desktop
                     │
        ┌────────────┴─────────────┐
        │                          │
   FastAPI Application      PostgreSQL Container (taskdb)
        │                          │
        └────────── TCP ───────────┘
               localhost:5432
                     │
               Docker Volume (taskdata)
                  taskdata
```

### Component Relationships & Connectivity

- **FastAPI Application:** Runs on the host machine and handles incoming client HTTP requests. It acts as the database client.
- **PostgreSQL Container (`taskdb`):** The database server runs isolated within this Docker container, managed by Docker Desktop.
- **localhost:5432:** Docker maps port `5432` of the container to port `5432` of the host computer, allowing the FastAPI application to establish a standard TCP connection to PostgreSQL using `localhost:5432`.
- **Docker Volume (`taskdata`):** PostgreSQL database files are not stored within the project directory. Instead, they are mounted to a Docker Volume (`taskdata`) which points to `/var/lib/postgresql/data` inside the container. This ensures data survives container restarts and deletions.
- **Environment Configuration:** The FastAPI application discovers and connects to the database via the `DATABASE_URL` environment variable loaded from the `.env` file.

---

## Why Docker & PostgreSQL?

Using Docker to containerize our PostgreSQL database solves several developer pain points:

- **Zero Manual Installation:** Developers do not need to install and configure PostgreSQL on their local machines.
- **Consistent Environments:** Every team member runs the exact same PostgreSQL version (v17), ensuring consistent behavior.
- **No "Works on My Machine" Issues:** Eliminates configuration differences between operating systems (Windows, macOS, Linux).
- **Portability & Reproducibility:** The database can be spun up or torn down with a single command, making onboarding instantaneous.

---

## Setting up PostgreSQL with Docker

To run the PostgreSQL database locally, use Docker to download the image, create the volume, and start the container.

### Setup Configuration Details
- **Docker Image:** `postgres:17`
- **Container Name:** `taskdb`
- **Host Port:** `5432`
- **Container Port:** `5432`
- **Docker Volume:** `taskdata`
- **Data Persistence:** Enabled via volume mounting.

### Initialization Command
Run the following command in your terminal to create and start the PostgreSQL container:

```bash
docker run --name taskdb \
  -e POSTGRES_PASSWORD=dev \
  -e POSTGRES_DB=tasks \
  -p 5432:5432 \
  -v taskdata:/var/lib/postgresql/data \
  -d postgres:17
```

---

## Connection String Breakdown

The FastAPI application uses the `DATABASE_URL` environment variable to connect to the database.

**Example Connection String:**
```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

| Part | Value | Description |
| :--- | :--- | :--- |
| **Protocol / Driver** | `postgresql` | Tells the client/SQLModel to connect using the PostgreSQL driver. |
| **Username** | `postgres` | Default administrative username for PostgreSQL. |
| **Password** | `dev` | The password configured when starting the container (`POSTGRES_PASSWORD`). |
| **Host** | `localhost` | The host address (since Docker maps the port to the host machine). |
| **Port** | `5432` | The mapped TCP port exposing PostgreSQL outside the container. |
| **Database Name** | `tasks` | The specific database within the PostgreSQL instance (`POSTGRES_DB`). |

---

## Migration from SQLite

Migrating to PostgreSQL has been completed with minimal impact on application code:
- **Storage Layer Isolation:** Only the database storage layer changed. 
- **Identical API Endpoints:** All API endpoints remain exactly the same.
- **Unchanged Message Formats:** Request bodies and JSON response payloads are unchanged.
- **Identical CRUD Behavior:** All behaviors (creation, update, statistics, filters) are completely identical.
- **SQLModel Adaptability:** Since SQLModel acts as a translation layer, the ORM queries automatically adapt from SQLite syntax to PostgreSQL syntax.

---

## Folder Structure

```
crud_api/
├── app/
│   ├── database/
│   │   └── task_db.py          # Engine, session factory, table creation (PostgreSQL)
│   ├── models/
│   │   └── task_model.py       # Pydantic / SQLModel schemas (Task, CreateTask, UpdateTask)
│   ├── repositories/
│   │   └── task_repo.py        # Raw database queries (all_task, get_id, insert_task, task_delete, get_stats)
│   ├── routes/
│   │   └── todo_route.py       # HTTP endpoint definitions
│   └── services/
│       └── task_service.py     # Business logic & error handling
├── main.py                     # FastAPI app entry point
├── pyproject.toml              # Dependencies & project metadata
├── .env.example                # Example environment variables file
├── .env                        # Local environment variables file (git-ignored)
└── README.md
```

### Architecture Flow

```
Client  →  Route (routes/)  →  Service (services/)  →  Repository (repositories/)  →  Database (database/)
```

---

## Getting Started

### 1. Prerequisite
Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 2. Set Up the Database
If you haven't created the PostgreSQL container yet, run the setup command:
```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:17
```

If you have already created the container, start it using:
```bash
docker start taskdb
```
*(Or, if a Docker Compose configuration is added in the future, run `docker compose up -d`)*

### 3. Configure Environment Variables
Create a local `.env` file in the root directory by copying the example template:
```bash
cp .env.example .env
```
Ensure the `DATABASE_URL` in `.env` matches your Docker container's configurations:
```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

### 4. Run the Application
Use `uv` (or pip) to install dependencies and run the server:
```bash
# Install dependencies
uv sync

# Start the server
uv run uvicorn main:app --reload
```

Server starts at **http://localhost:8000**.  
Swagger docs at **http://localhost:8000/docs**.

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

Both implemented the same 7 CRUD + health + stats operations, originally on SQLite (and now migrated to PostgreSQL). Below is a side-by-side analysis of the initial code implementations.

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
