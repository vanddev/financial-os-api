# Financial OS API

Personal Finance Platform - A comprehensive financial management system for families.

## Objective

Financial OS API is a complete financial management system designed to help families track and manage their finances. The system provides a robust foundation for building financial features including accounts, transactions, investments, goals, analytics, and more.

## Technologies

- **Python 3.13+**
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy 2** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **PostgreSQL** - Relational database
- **Pydantic v2** - Data validation using Python type annotations
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Pytest** - Testing framework
- **Ruff** - Fast Python linter and formatter
- **MyPy** - Static type checker
- **Uvicorn** - ASGI server
- **uv** - Fast Python package manager

## Project Structure

```
financial-os-api/
├── app/
│   ├── modules/           # Domain modules
│   │   └── health/        # Health check module
│   ├── core/              # Core application components
│   │   ├── config.py      # Configuration management
│   │   ├── database.py    # Database configuration
│   │   ├── logging.py     # Logging setup
│   │   ├── exceptions.py  # Exception handlers
│   │   └── lifespan.py    # Application lifecycle
│   ├── shared/            # Shared utilities
│   │   ├── middleware/    # Custom middleware
│   │   ├── responses/     # Standardized API responses
│   │   ├── pagination/    # Pagination utilities
│   │   └── utils/         # Common utilities
│   ├── db/                # Database-related code
│   ├── tests/             # Test files
│   └── main.py            # Application entry point
├── alembic/               # Database migrations
├── docker/                # Docker-related files
├── scripts/               # Utility scripts
├── .env.example           # Environment variables template
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose
- uv (Python package manager)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-os-api
```

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Install dependencies:
```bash
uv sync
```

4. Copy environment file:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```bash
APP_NAME=Financial OS API
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_os
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/financial_os

LOG_LEVEL=INFO
```

## Running the Application

### Using Docker Compose (Recommended)

1. Start all services:
```bash
docker compose up
```

2. The API will be available at `http://localhost:8000`
3. API documentation (Swagger UI) at `http://localhost:8000/docs`
4. pgAdmin available at `http://localhost:5050` (email: admin@financial-os.local, password: admin)

### Local Development

1. Start PostgreSQL (using Docker):
```bash
docker compose up postgres pgadmin
```

2. Run the application:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

The workflow `.github/workflows/publish-image.yml` builds the `production` stage from
the `Dockerfile` and publishes it to GitHub Container Registry (GHCR):

```text
ghcr.io/<github-owner>/financial-os-api:latest
ghcr.io/<github-owner>/financial-os-api:v1.0.0
ghcr.io/<github-owner>/financial-os-api:sha-<commit>
```

Pushes to `main` publish `latest` and a commit tag. Tags matching `v*` also publish
the corresponding version. The workflow can also be started manually from GitHub Actions.

### Configure the VPS

Copy `compose.production.yml` to the VPS and create a `.env` file in the same directory:

```bash
GHCR_IMAGE=ghcr.io/<github-owner>/financial-os-api
IMAGE_TAG=v1.0.0

APP_NAME=Financial OS API
APP_VERSION=1.0.0
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=financial_os
POSTGRES_USER=financial_os
POSTGRES_PASSWORD=<strong-password>
```

Keep this `.env` file only on the VPS and do not commit production credentials. Prefer an
immutable version such as `v1.0.0` or `sha-<commit>` for `IMAGE_TAG` instead of `latest`.

If the GHCR package is private, create a GitHub personal access token with `read:packages`
and authenticate Docker on the VPS once:

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io \
  --username <github-user> \
  --password-stdin
```

Public GHCR packages can be pulled without authentication.

### Recommended production publication order

1. Run the application checks locally:

```bash
uv run ruff check .
uv run mypy app/
uv run pytest
```

2. Commit the release and create a version tag:

```bash
git add .
git commit -m "chore: release v1.0.0"
git tag v1.0.0
git push origin main
git push origin v1.0.0
```

3. Wait for the `Publish container image` workflow to complete successfully in GitHub
Actions.

4. On the VPS, set `IMAGE_TAG` in `.env` to the published version and download the image:

```bash
docker compose -f compose.production.yml pull
```

5. Apply database migrations using the new image:

```bash
docker compose -f compose.production.yml run --rm api \
  uv run --no-sync alembic upgrade head
```

6. Start or replace the application containers:

```bash
docker compose -f compose.production.yml up -d
```

7. Verify container status, logs, and the health endpoint:

```bash
docker compose -f compose.production.yml ps
docker compose -f compose.production.yml logs --tail=100 api
curl --fail http://127.0.0.1:8000/health
```

To roll back the application image, restore the previous `IMAGE_TAG`, then repeat `pull`
and `up -d`. Database rollback must be evaluated separately before running any Alembic
downgrade.

## Database Migrations

### Create a new migration

```bash
uv run alembic revision --autogenerate -m "description of changes"
```

### Apply migrations

```bash
uv run alembic upgrade head
```

### Rollback migrations

```bash
uv run alembic downgrade -1
```

### View migration history

```bash
uv run alembic history
```

### View current migration status

```bash
uv run alembic current
```

### Populate database with mock data

```bash
python scripts/seed_financial.py
```

## Running Tests

### Run all tests

```bash
uv run pytest
```

### Run with coverage

```bash
uv run pytest --cov=app --cov-report=html
```

### Run specific test file

```bash
uv run pytest app/tests/test_health.py
```

### Run with verbose output

```bash
uv run pytest -v
```

## Code Quality

### Linting with Ruff

```bash
uv run ruff check .
```

### Auto-fix linting issues

```bash
uv run ruff check --fix .
```

### Format code with Ruff

```bash
uv run ruff format .
```

### Type checking with MyPy

```bash
uv run mypy app/
```

## Adding New Modules

1. Create a new module directory under `app/modules/`:
```bash
mkdir -p app/modules/your_module
```

2. Create the module structure:
```bash
touch app/modules/your_module/__init__.py
touch app/modules/your_module/router.py
touch app/modules/your_module/models.py
touch app/modules/your_module/schemas.py
touch app/modules/your_module/services.py
```

3. Define your FastAPI router in `router.py`:
```python
from fastapi import APIRouter

router = APIRouter(prefix="/your-module", tags=["your-module"])

@router.get("/")
async def get_items():
    return {"message": "Your module endpoint"}
```

4. Export the router in `__init__.py`:
```python
from app.modules.your_module.router import router

__all__ = ["router"]
```

5. Register the router in `app/main.py`:
```python
from app.modules.your_module import router as your_module_router

app.include_router(your_module_router)
```

6. Create database models in `models.py` (if needed):
```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class YourModel(Base):
    __tablename__ = "your_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
```

7. Create Pydantic schemas in `schemas.py`:
```python
from pydantic import BaseModel

class YourSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
```

8. Create business logic in `services.py`:
```python
from sqlalchemy.orm import Session
from app.modules.your_module.models import YourModel
from app.modules.your_module.schemas import YourSchema

def create_item(db: Session, item_data: dict) -> YourSchema:
    db_item = YourModel(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return YourSchema.model_validate(db_item)
```

9. Create tests in `app/tests/test_your_module.py`:
```python
from httpx import AsyncClient
from app.main import app

async def test_your_module_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/your-module/")
        assert response.status_code == 200
```

## API Endpoints

### Root Endpoint
- **GET** `/` - Returns application information
  ```json
  {
    "application": "Financial OS API",
    "version": "1.0.0",
    "status": "running"
  }
  ```

### Health Check
- **GET** `/health` - Health check endpoint
  ```json
  {
    "status": "healthy"
  }
  ```

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options:

- `APP_NAME` - Application name
- `APP_VERSION` - Application version
- `ENVIRONMENT` - Environment (development/production)
- `DEBUG` - Debug mode
- `POSTGRES_HOST` - PostgreSQL host
- `POSTGRES_PORT` - PostgreSQL port
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `DATABASE_URL` - Full database connection string
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Architecture Principles

This project follows clean architecture principles with:

- **Separation of concerns** - Clear separation between API, services, and persistence
- **Domain-driven design** - Organization by domain modules
- **Dependency injection** - Using FastAPI's dependency system
- **Type safety** - Full type annotations with MyPy checking
- **Simplicity** - Avoiding overengineering and unnecessary abstractions

## Development Guidelines

- Follow the existing code style and patterns
- Add type hints to all functions
- Write tests for new features
- Run linting and type checking before committing
- Keep functions small and focused
- Use meaningful variable and function names
- Add docstrings for complex functions
- Follow PEP 8 style guide (enforced by Ruff)

## License

[Specify your license here]

## Contributing

[Specify contribution guidelines here]
