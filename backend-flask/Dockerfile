# Build stage
FROM python:3.12-slim as development

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry using pip
RUN pip install poetry==1.7.1

# Install test dependencies first
RUN poetry add --group dev pytest-asyncio pytest-cov

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy source code
COPY . .

# Create static directory for Swagger
RUN mkdir -p app/static

# Expose port
EXPOSE 5000

# Run the development server
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--reload"]

# Test stage (single definition)
FROM development as test
COPY tests/ /app/tests/
CMD ["poetry", "run", "pytest"]

# Production stage
FROM python:3.12-slim as production

WORKDIR /app

# Install system dependencies and poetry
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry==1.7.1

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies (production only)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Copy source code
COPY . .

# Run the production server
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"] 