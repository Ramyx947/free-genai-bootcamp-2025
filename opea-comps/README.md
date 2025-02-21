# OpenAI Components (opea-comps)

A Python package for orchestrating microservices for AI components.

## Table of Contents
- [Installation](#installation)
- [Development Setup](#development-setup)
- [Docker Setup](#docker-setup)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package
pip install -e .
```

## Development Setup

```bash
# Install dependencies
pip install -e .

# Run tests
python tests/test_service.py
```

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Building and Running with Docker

1. Build all services:
```bash
docker-compose build
```

2. Start all services:
```bash
# Regular mode
docker-compose up

# Detached mode
docker-compose up -d
```

3. Development mode with hot-reload:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

4. View logs:
```bash
docker-compose logs -f
```

5. Stop services:
```bash
docker-compose down
```

### Service Ports
- Embedding Service: `6000`
- LLM Service: `9000`
- Mega Service: `8000`

### Environment Variables
```env
EMBEDDING_SERVICE_HOST_IP=embedding
EMBEDDING_SERVICE_PORT=6000
LLM_SERVICE_HOST_IP=llm
LLM_SERVICE_PORT=9000
```

## Project Structure
```
opea-comps/
├── src/
│   └── comps/
│       ├── __init__.py
│       ├── __main__.py
│       └── service.py
├── tests/
│   └── test_service.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── .dockerignore
└── pyproject.toml
```

## Testing

```bash
# Run tests
python tests/test_service.py
```

## License

[Add your license information here] 