# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set security-related environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5001 \
    POETRY_NO_INTERACTION=1

# Expose port
EXPOSE ${PORT}

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5001"] 