# Build stage
FROM python:3.12-slim as development

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry using pip (more reliable than the installer script)
RUN pip install poetry==1.7.1

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

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"] 