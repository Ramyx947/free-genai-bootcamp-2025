# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy only dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --without dev

# Runtime stage
FROM python:3.12-slim

# Create non-root user
RUN useradd -m -r -u 1001 appuser

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY vocab_importer ./vocab_importer

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
CMD ["python", "-m", "vocab_importer.main"] 