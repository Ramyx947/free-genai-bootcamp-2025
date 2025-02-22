# OpenAI Components (opea-comps)

A simple tool that connects different AI services together.

## What It Does

This tool has 3 main services:
1. Embedding Service (port 6000) - Turns text into numbers
2. LLM Service (port 9000) - Generates text responses
3. Mega Service (port 8000) - Connects the other services together

## Quick Start

1. Start all services:
```bash
docker-compose up
```

2. Wait until you see "Application startup complete" messages

## Testing the Services

You can test each service with these commands:

### 1. Test Embedding Service
```bash
curl -X POST http://localhost:6000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-ada-002", "messages": "Hello, world!"}'
```

### 2. Test LLM Service
```bash
curl -X POST http://localhost:9000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "model": "test-model"
  }'
```

### 3. Test Mega Service
```bash
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "model": "test-model"
  }'
```

## Check Service Status

Open these links in your browser:
- http://localhost:6000/ - See Embedding Service info
- http://localhost:9000/ - See LLM Service info
- http://localhost:8000/ - See Mega Service info

## Stopping Services

When you're done:
```bash
docker-compose down
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

## Testing

```bash
# Run tests
python tests/test_service.py
```