# Restaurant Cloud Platform API

Sprint 1 - Foundation

## Requirements
- Docker
- Docker Compose

## Getting Started

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Start the services:
   ```bash
   docker-compose up -d --build
   ```

3. Run migrations:
   ```bash
   docker-compose exec api alembic upgrade head
   ```

## Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
