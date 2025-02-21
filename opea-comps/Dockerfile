# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y \
    build-essential \
    curl

# Install poetry
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "comps"] 