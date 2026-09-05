# MeetAI

MeetAI is a real-time AI meeting platform. The Day 1 repository foundation establishes the React/Vite frontend, FastAPI backend, PostgreSQL persistence layer, Redis/Celery worker infrastructure, WebSocket transport path, and Nginx ingress. Application features are intentionally deferred to later implementation days.

## Architecture

```text
Browser -> Nginx -> React frontend
                 -> FastAPI (/api, /ws)
                      -> PostgreSQL
                      -> Redis -> Celery worker
```

The backend is organized into API, core infrastructure, models, schemas, services, repositories, WebSocket, and worker layers. Routes are versioned under `/api/v1`; business logic and database access will be added as individual features are implemented.

## Technology stack

- Backend: Python 3.12+, FastAPI, SQLAlchemy 2.x, Pydantic v2, Alembic, Pytest
- Frontend: React 18, TypeScript (strict), Vite, React Router, Tailwind CSS, Axios
- Infrastructure: PostgreSQL 16, Redis 7, Celery, Docker Compose, Nginx

## Repository structure

```text
backend/
  app/{api,core,models,schemas,services,repositories,websocket,workers}/
  alembic/                 # Migration environment and future revisions
  tests/                   # Backend tests
frontend/
  src/{components,pages,features,hooks,services,types}/
nginx/nginx.conf           # /, /api, and /ws routing
docker-compose.yml
.env.example
```

## Local setup

1. Copy `.env.example` to `.env` and replace the placeholder secrets.
2. Start PostgreSQL and Redis:

   ```bash
   docker compose up -d db redis
   ```

3. Create a backend environment and install dependencies:

   ```bash
   cd backend
   python -m venv .venv
   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

4. In another terminal, install and run the frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The backend health endpoint is `http://localhost:8000/health`. The versioned foundation endpoint is `http://localhost:8000/api/v1`.

## Docker setup

Build and start the complete foundation:

```bash
docker compose up --build
```

Open `http://localhost`. Nginx serves the frontend and proxies `/api` and `/ws` to FastAPI. The backend and Celery worker share the same image and environment. Stop services with `docker compose down`; add `-v` only when you intentionally want to remove local database and Redis volumes.

## Environment variables

See [.env.example](.env.example) for the documented template. Required areas are PostgreSQL connection details, Redis URL, JWT settings, and service/CORS URLs. Never commit `.env` or real secrets.

## Tests and validation commands

Backend tests:

```bash
cd backend
pytest -v
```

Frontend build:

```bash
cd frontend
npm run build
```

Alembic is ready for future revisions:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## Future implementation placeholders

The next phases will add JWT registration/login and refresh-token rotation, meeting lifecycle APIs, persisted chat and presence, Redis pub/sub, validated audio uploads, Celery transcription and AI summaries, searchable history, security hardening, comprehensive tests, and production HTTPS configuration. WebRTC video/audio, calendar synchronization, diarization, vector search, live voice agents, enterprise SSO, and advanced analytics remain outside the initial scope.
