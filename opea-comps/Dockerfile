# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction

# Copy application code
COPY . .

# Runtime command based on service type
CMD ["python", "-m", "comps"]

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Copy project files
COPY pyproject.toml poetry.lock* README.md ./
COPY comps ./comps
COPY tests ./tests

# Install poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --with dev

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "comps"] 