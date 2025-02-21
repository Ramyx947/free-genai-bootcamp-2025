# Romanian Learning Application

## Project Overview
A full-stack application for learning Romanian vocabulary with interactive features and AI assistance.

## Architecture
```
project/
├── frontend-react/        # React frontend (Port 5173)
├── backend-flask/         # Flask API backend (Port 5000)
├── opea-comps/           # OpenAI components
│   ├── embedding/        # Embedding Service (Port 6000)
│   ├── llm/             # LLM Service (Port 9000)
│   └── mega/            # Mega Service (Port 8000)
├── docker-compose.yml    # Development compose
└── docker-compose.dev.yml # Development overrides
```

## Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.12+ (for local development)

## Quick Start
```bash
# Development with hot-reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production deployment
docker compose -f docker-compose.prod.yml up -d
```

## Development Features

### Hot-Reloading
- Frontend: Component changes, styles, assets
- Backend: Routes, API, configurations
- OpenAI Components: Service logic, configs

### Volume Mounts
```yaml
volumes:
  - ./frontend-react:/app        # React source
  - /app/node_modules           # Node modules
  - ./backend-flask:/app        # Flask source
  - /app/.venv                 # Python environment
```

## Docker Best Practices
- Multi-stage builds for optimized images
- Cached dependency installation
- Development/Production environment separation
- BuildKit cache mounts
- Health checks for service availability
- CORS security configuration
- Parallel builds support

## Service Integration
- Frontend ↔️ Backend API communication
- Backend ↔️ OpenAI services coordination
- Swagger UI documentation at `/docs`

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

For detailed documentation:
- [Frontend Documentation](./frontend-react/README.md)
- [Backend Documentation](./backend-flask/README.md)
- [OpenAI Components](./opea-comps/README.md)
