# Backend: Code Challenge Poll (FastAPI)

A small API for polls: questions, answers, and view statistics.  
Built with FastAPI + SQLModel, using SQLite by default. Dependencies and execution are managed with `uv`.

Links:
- OpenAPI docs: `http://localhost:8000/docs` and `http://localhost:8000/redoc`
- FastAPI project: https://fastapi.tiangolo.com
- Package manager `uv`: https://github.com/astral-sh/uv

## Requirements
- Python 3.12+
- Installed `uv` (see installation guide in the `uv` repository)
- Alternative: Docker

## Quick start (local)
From the `be/` directory:

```bash
# Install dependencies and create .venv
uv sync

# Run dev server with auto‑reload
uv run fastapi dev --host 0.0.0.0 --port 8000
```

By default, the `SQLite` database is created in the file `be/database.db` on application startup.  
Migrations are not required — `SQLModel` creates tables automatically.

Activate the virtual environment if needed:
```bash
source .venv/bin/activate
```

## Production run
```bash
uv run fastapi run --host 0.0.0.0 --port 8000
```

## Run with Docker
From the repository root:
```bash
docker build -t poll-be -f be/Dockerfile be
docker run --rm -p 8000:8000 \
  -e CORS_ORIGINS="http://localhost,http://localhost:5173" \
  -e DATABASE_URL="sqlite:////app/database.db" \
  poll-be
```

## Environment variables
- `CORS_ORIGINS`: comma‑separated list of allowed CORS domains.  
  - Default: `http://localhost,http://localhost:8080,http://localhost:5173`
- `DATABASE_URL`: SQLAlchemy connection string.  
  - Default: `sqlite:///database.db` (file in the `be/` directory)

## Structure
- `be/main.py`: FastAPI entry points and routes
- `be/models.py`: SQLModel models and request/response schemas
- `be/db.py`: engine/session setup and table creation
- `be/pyproject.toml`: project dependencies (`fastapi[standard]`, `sqlmodel`)
- `be/Dockerfile`: image based on `ghcr.io/astral-sh/uv`

## Development
- Formatting: `uv run black .` and `uv run isort .`
- Reset database: stop the server and remove the file `be/database.db`
