# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
# Prevents Python from writing .pyc files to container disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr, making logs appear in real-time
ENV PYTHONUNBUFFERED=1

# Install system dependencies required to build packages like psycopg2 (C-extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (astral-sh package manager) directly from the official Docker image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Copy dependency definition files to cache installation layer
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv (fast, locked dependencies)
RUN uv sync --frozen --no-cache

# Copy the rest of the application files
COPY . .

# Expose the application port inside the container
EXPOSE 8000

# Add the virtual environment's bin directory to PATH so we don't need "uv run"
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
