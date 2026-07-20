

Build a production-quality RESTful CRUD API using Python, FastAPI, and Pydantic (or SQLModel if appropriate for request/response models). The primary goal is to create a clean, well-structured backend application that correctly implements all CRUD operations with proper validation, error handling, and HTTP status codes.

## Functional Requirements

Build an API for managing a resource (for example, Books). The API must support the following operations:

  1.  Create a new record (POST)
  2.  Retrieve all records (GET)
  3. Retrieve a single record by its ID (GET)
  4.  Update an existing record (PUT)
  5. Delete a record (DELETE)


## Technical Requirements

Use Python, FastAPI and UV as a project manager .
Use Pydantic models (or SQLModel) for request validation and response models.
Organize the code using clean project structure and good coding practices.
Use SQLite as the database with SQLAlchemy or SQLModel for persistence.
Automatically create database tables on application startup.
Implement proper database sessions and dependency injection.
Keep the code modular, readable, and maintainable.