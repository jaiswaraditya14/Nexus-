# MeetAI — Getting Started & Build Instructions

Welcome to the **MeetAI** project! This guide provides a complete, step-by-step roadmap and actionable developer instructions to start building the MeetAI platform from ground zero to production deployment.

---

## Table of Contents
1. [Project Overview & Core Architecture](#1-project-overview--core-architecture)
2. [Prerequisites & Development Environment](#2-prerequisites--development-environment)
3. [Target Repository Structure](#3-target-repository-structure)
4. [Phase 0: Initial Project Bootstrapping (Day 1)](#4-phase-0-initial-project-bootstrapping-day-1)
   - [4.1 Backend Setup (FastAPI)](#41-backend-setup-fastapi)
   - [4.2 Frontend Setup (React + Vite + TypeScript)](#42-frontend-setup-react--vite--typescript)
   - [4.3 Local Infrastructure (Docker Compose for Postgres & Redis)](#43-local-infrastructure-docker-compose-for-postgres--redis)
   - [4.4 Environment Configuration (`.env`)](#44-environment-configuration-env)
5. [Day-by-Day Implementation Roadmap (15-Day Plan)](#5-day-by-day-implementation-roadmap-15-day-plan)
6. [Daily Development Commands](#6-daily-development-commands)
7. [Architectural Rules & Coding Standards](#7-architectural-rules--coding-standards)
8. [Scope Guardrails (What NOT to Build)](#8-scope-guardrails-what-not-to-build)
9. [AI-Assisted Vibe-Coding Prompts](#9-ai-assisted-vibe-coding-prompts)

---

## 1. Project Overview & Core Architecture

**MeetAI** is a production-ready, full-stack real-time meeting intelligence platform.

### High-Level Architecture Flow
```text
Client Browser (React + TypeScript + Vite + Tailwind CSS)
   │
   ├── REST API (HTTP) ───────────► [ Nginx Ingress ] ──► [ FastAPI Backend ] ──► [ PostgreSQL ]
   │                                                             │
   ├── Real-Time Chat (WebSocket) ─► [ Nginx Ingress ] ──────────┤
   │                                                             │
   └── Audio Upload (REST) ───────► [ Nginx Ingress ] ───────────┤
                                                                 ▼
                                                         [ Redis Broker ]
                                                                 │
                                                                 ▼
                                                         [ Celery Worker ]
                                                                 │
                                                      ┌──────────┴──────────┐
                                                      ▼                     ▼
                                              OpenAI Whisper        OpenAI GPT-4o
                                            (Audio Transcription)  (Summaries & Tasks)
                                                      │                     │
                                                      └──────────┬──────────┘
                                                                 ▼
                                                         [ PostgreSQL ]
```

### Core Stack
* **Frontend**: React 18+, TypeScript, Vite, Tailwind CSS, Lucide React, React Router v6.
* **Backend**: FastAPI (Python 3.11+), Pydantic v2, SQLAlchemy 2.x, Alembic.
* **Real-time**: WebSockets (FastAPI Native) + Redis Pub/Sub.
* **Async Workers**: Celery + Redis.
* **Database**: PostgreSQL 16+.
* **AI Engine**: OpenAI Whisper (transcription) + GPT-4o / GPT-4o-mini (summaries & action items).
* **Ingress & Deploy**: Docker Compose + Nginx (HTTPS, WebSocket proxying).

---

## 2. Prerequisites & Development Environment

Before writing code, ensure the following tools are installed on your machine:

1. **Python 3.11 or higher**
   - Verify: `python --version`
2. **Node.js 18+ or 20+ (LTS) & npm**
   - Verify: `node -v` and `npm -v`
3. **Docker Desktop & Docker Compose v2**
   - Verify: `docker --version` and `docker compose version`
4. **Git**
   - Verify: `git --version`
5. **OpenAI API Key**
   - An active API key with access to Whisper and GPT models.

---

## 3. Target Repository Structure

Organize the repository cleanly from Day 1 to avoid refactoring later:

```text
meetai/
├── backend/
│   ├── app/
│   │   ├── api/             # REST route handlers & WebSocket endpoints
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── meetings.py
│   │   │   │   ├── audio.py
│   │   │   │   └── search.py
│   │   │   └── websocket.py # WebSocket router & endpoints
│   │   ├── core/            # Config, security (JWT, hashing), DB session, Celery init
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── database.py
│   │   │   └── celery_app.py
│   │   ├── models/          # SQLAlchemy 2.x ORM models
│   │   │   ├── user.py
│   │   │   ├── meeting.py
│   │   │   ├── message.py
│   │   │   ├── transcript.py
│   │   │   └── summary.py
│   │   ├── schemas/         # Pydantic v2 request/response/event schemas
│   │   │   ├── user.py
│   │   │   ├── meeting.py
│   │   │   ├── message.py
│   │   │   ├── transcript.py
│   │   │   └── websocket.py
│   │   ├── services/        # Business logic operations
│   │   │   ├── auth_service.py
│   │   │   ├── meeting_service.py
│   │   │   └── ai_service.py
│   │   ├── repositories/    # Database query abstraction
│   │   ├── websocket/       # ConnectionManager & room broadcaster
│   │   │   ├── manager.py
│   │   │   └── events.py
│   │   ├── workers/         # Celery background tasks
│   │   │   ├── tasks.py
│   │   │   └── audio_processor.py
│   │   └── main.py          # FastAPI application factory
│   ├── alembic/             # Database migrations
│   ├── tests/               # Pytest suite (unit, api, db, ws, workers)
│   ├── requirements.txt
│   ├── alembic.ini
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI elements (Button, Modal, Input, Badge)
│   │   ├── pages/           # Route views (Login, Register, Dashboard, Room, History)
│   │   ├── features/        # Chat, Transcription Viewer, Summary Cards
│   │   ├── hooks/           # useAuth, useWebSocket, useMeeting
│   │   ├── services/        # Axios / Fetch API client functions
│   │   ├── types/           # TypeScript interfaces matching backend models
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── Dockerfile
├── nginx/
│   └── nginx.conf           # Reverse proxy routing (/api, /ws, /)
├── docker-compose.yml       # Local & production multi-container setup
├── .env.example             # Documented template of environment variables
└── README.md
```

---

## 4. Phase 0: Initial Project Bootstrapping (Day 1)

Follow these direct steps to scaffold and verify your foundation.

### 4.1 Backend Setup (FastAPI)

1. **Create the backend folder and Python virtual environment**:
   ```bash
   mkdir -p backend/app
   cd backend
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Create `backend/requirements.txt`**:
   ```text
   fastapi>=0.110.0
   uvicorn[standard]>=0.28.0
   pydantic>=2.6.0
   pydantic-settings>=2.2.0
   sqlalchemy>=2.0.28
   alembic>=1.13.1
   asyncpg>=0.29.0
   psycopg2-binary>=2.9.9
   python-jose[cryptography]>=3.3.0
   passlib[bcrypt]>=1.7.4
   bcrypt>=4.0.1
   python-multipart>=0.0.9
   celery>=5.3.6
   redis>=5.0.3
   openai>=1.14.0
   httpx>=0.27.0
   pytest>=8.1.0
   pytest-asyncio>=0.23.5
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Alembic**:
   ```bash
   alembic init alembic
   ```

5. **Create minimal `backend/app/main.py`**:
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware

   app = FastAPI(title="MeetAI API", version="1.0.0")

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:5173"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

   @app.get("/health")
   def health_check():
       return {"status": "healthy", "service": "meetai-backend"}

   @app.get("/api/health")
   def api_health_check():
       return {"status": "healthy", "version": "1.0.0"}
   ```

6. **Test backend locally**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *Verify*: Open `http://localhost:8000/health` in your browser.

---

### 4.2 Frontend Setup (React + Vite + TypeScript)

1. **Initialize the Vite React project in the repository root**:
   ```bash
   cd .. # Back to project root
   npm create vite@latest frontend -- --template react-ts
   cd frontend
   npm install
   ```

2. **Install UI & utility libraries**:
   ```bash
   npm install react-router-dom axios lucide-react clsx tailwind-merge
   npm install -D tailwindcss postcss autoprefixer @types/node
   npx tailwindcss init -p
   ```

3. **Configure `frontend/tailwind.config.js`**:
   ```javascript
   /** @type {import('tailwindcss').Config} */
   export default {
     content: [
       "./index.html",
       "./src/**/*.{js,ts,jsx,tsx}",
     ],
     theme: {
       extend: {
         colors: {
           brand: {
             50: '#eef2ff',
             500: '#6366f1',
             600: '#4f46e5',
             700: '#4338ca',
             900: '#312e81',
           }
         }
       },
     },
     plugins: [],
   }
   ```

4. **Add Tailwind directives to `frontend/src/index.css`**:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

5. **Test frontend locally**:
   ```bash
   npm run dev
   ```
   *Verify*: Open `http://localhost:5173` in your browser.

---

### 4.3 Local Infrastructure (Docker Compose for Postgres & Redis)

Create `docker-compose.yml` in the project root to run PostgreSQL and Redis locally with persistent volumes:

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: meetai_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgrespassword
      POSTGRES_DB: meetai_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: meetai_redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Start the infrastructure**:
```bash
docker compose up -d db redis
```

---

### 4.4 Environment Configuration (`.env`)

Create `.env.example` in the project root (and copy to `.env`):

```bash
# Database
DATABASE_URL=postgresql://postgres:postgrespassword@localhost:5432/meetai_db

# Redis & Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security / JWT
JWT_SECRET_KEY=change_this_to_a_secure_random_hex_string_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Audio File Storage
AUDIO_UPLOAD_DIR=./uploads/audio
MAX_UPLOAD_SIZE_MB=25

# App Settings
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 5. Day-by-Day Implementation Roadmap (15-Day Plan)

| Day | Phase | Deliverables & Tasks | Verification / Exit Criteria |
| :---: | :--- | :--- | :--- |
| **Day 1** | **Foundation** | Scaffold backend, frontend, docker-compose (DB + Redis), `.env`, health endpoints. | `GET /health` returns 200; Vite loads on port 5173; containers healthy. |
| **Day 2** | **Database Layer** | Define SQLAlchemy 2.x models (`User`, `Meeting`, `Message`, `Transcript`, `Summary`, `ActionItem`); create initial Alembic migration; build Pydantic schemas. | `alembic upgrade head` runs cleanly; tables and foreign keys exist in PostgreSQL. |
| **Day 3** | **Auth Subsystem** | User registration, password hashing (bcrypt), login endpoint, JWT access & refresh token rotation, logout revocation, `/me` endpoint, React protected routes. | Postman/curl can register, login, refresh token, access protected route; unauthorized requests return 401. |
| **Day 4** | **Meetings Management** | Meeting CRUD: create, list, view detail, join, leave, cancel, archive; Dashboard UI with meeting listings and status badges. | Users can create meetings, see them on React Dashboard, and view meeting room metadata. |
| **Day 5** | **WebSocket Base** | FastAPI WebSocket endpoint with token authentication; in-memory `ConnectionManager`; join/leave room lifecycle; error event handling. | Two browser tabs connect via WebSocket, receive `connection.join` confirmation, and disconnect gracefully. |
| **Day 6** | **Chat & Presence** | Real-time chat messages broadcast across room; chat persistence into `messages` table; typing indicators (`typing.start`/`stop`); participant presence list. | Two users chat in real time; chat history persists upon page refresh; active participants shown. |
| **Day 7** | **Redis & Reliability** | Connect Redis Pub/Sub to WebSocket manager for multi-process broadcasting; client auto-reconnect with exponential backoff; heartbeat ping/pong. | Stopping and restarting backend recovers connection; message broadcast works across multiple worker processes. |
| **Day 8** | **Audio Upload & Celery** | Multipart audio upload endpoint (`POST /api/meetings/{id}/audio`); file validation (MP3/WAV, ≤25MB); create Celery worker instance; persist `UPLOADED` transcript record. | Uploading an audio file creates an `UPLOADED` transcript row and enqueues Celery task. |
| **Day 9** | **Whisper Transcription** | Celery task calls OpenAI Whisper; parse response into `raw_text` and timestamped `transcript_segments`; update status to `PROCESSING` -> `COMPLETED`. | Audio is converted to transcript segments in DB; frontend renders timestamped transcript list. |
| **Day 10** | **AI Intelligence** | Celery task calls OpenAI GPT-4o with structured prompt; extracts overview, key decisions, and action items; stores in `meeting_summaries` and `action_items`. | Meeting page displays formatted summary card, bulleted decisions, and actionable task checkboxes. |
| **Day 11** | **History & Search** | Paginated meeting history page; full-text search across meeting titles and transcript segments (`GET /api/search?q=...`); filter by date/status. | Searching for a spoken keyword returns relevant meetings and highlights matching transcript segments. |
| **Day 12** | **Security Hardening** | Rate limiting on auth/upload endpoints; CORS hardening; input sanitization; authorization checks (ensure only room participants access transcripts); sanitize stack traces. | Non-participants receive 403 Forbidden when accessing another meeting's transcripts/audio. |
| **Day 13** | **Automated Testing** | Pytest suites for Auth, Meeting CRUD, WebSocket events, Celery mock tasks; frontend component tests; critical E2E path test. | `pytest` runs with >80% pass rate across core modules; no regressions. |
| **Day 14** | **Docker & Nginx** | Full production `docker-compose.yml` (frontend, backend, celery, db, redis, nginx); configure `nginx.conf` for reverse proxy and WebSocket upgrade. | Single `docker compose up` starts entire application reachable on `http://localhost`. |
| **Day 15** | **Portfolio Polish** | Visual UI polish, dark/light styling, README with architecture diagrams, performance metric logging, technical interview flashcard review. | Application is fully presentable with working demo, clean commit history, and zero dead code. |

---

## 6. Daily Development Commands

Keep these commands handy during daily development:

### Running Services Locally (Development Mode)

```bash
# 1. Start PostgreSQL & Redis
docker compose up -d db redis

# 2. Start Backend (Terminal 1)
cd backend
source venv/bin/activate  # Or .\venv\Scripts\Activate.ps1 on Windows
uvicorn app.main:app --reload --port 8000

# 3. Start Celery Worker (Terminal 2)
cd backend
source venv/bin/activate
celery -A app.core.celery_app.celery worker --loglevel=info

# 4. Start Frontend Dev Server (Terminal 3)
cd frontend
npm run dev
```

### Database Migrations (Alembic)

```bash
cd backend
# Create a new revision after updating SQLAlchemy models
alembic revision --autogenerate -m "create_initial_models"

# Apply migrations
alembic upgrade head

# Rollback one revision (if needed)
alembic downgrade -1
```

### Running Tests

```bash
cd backend
# Run all tests
pytest -v

# Run with coverage report
pytest --cov=app tests/
```

---

## 7. Architectural Rules & Coding Standards

To maintain clean code and pass technical reviews, strictly adhere to these rules:

1. **Strict Layer Separation**:
   - **Routes** (`app/api/`): HTTP parsing, status codes, dependency injection. No raw DB queries.
   - **Services** (`app/services/`): Business logic, orchestration, validation rules.
   - **Repositories** (`app/repositories/`): SQLAlchemy queries and data persistence only.
   - **Schemas** (`app/schemas/`): Pydantic v2 models for input/output serialization.
   - **Models** (`app/models/`): SQLAlchemy 2.x declarative models.
2. **Never Run AI or Transcoding in FastAPI Routes**:
   - Audio transcription and GPT calls take seconds to minutes. Always dispatch them to Celery background tasks.
3. **Idempotent Background Jobs**:
   - Check status before processing. If a task retries, ensure it does not duplicate segment rows or summary records.
4. **Type Safety Across Both Stacks**:
   - Backend: Use Python type hints (`mypy`-compliant).
   - Frontend: Strict TypeScript (`"strict": true` in `tsconfig.json`). No `any` types.
5. **Atomic Transactions**:
   - Wrap multi-table operations (e.g., creating a meeting and adding the owner as a participant) in an atomic database session transaction.
6. **No Leaking Secrets or Stacks**:
   - Return clean HTTP exceptions (`HTTPException(status_code=400, detail="...")`). Never leak database exceptions or API keys to the frontend.

---

## 8. Scope Guardrails (What NOT to Build)

To ensure timely delivery, the following features are **explicitly out of scope**:

| Excluded Feature | What to Do Instead |
| :--- | :--- |
| ❌ Live WebRTC peer-to-peer video/audio | ✅ Audio file upload + asynchronous background transcription. |
| ❌ Google Calendar / Outlook sync | ✅ In-app meeting scheduling and status tracking. |
| ❌ Enterprise SSO (SAML / Okta) | ✅ Standard JWT access & refresh token authentication. |
| ❌ Speaker Diarization (Who spoke when) | ✅ Segment-level timestamped transcripts. |
| ❌ Live in-meeting AI voice assistant | ✅ Post-meeting automated summary and action-item generation. |
| ❌ Vector Database / Pinecone / RAG | ✅ PostgreSQL text and metadata search with pagination. |

---

## 9. AI-Assisted Vibe-Coding Prompts

Use these exact prompts when delegating tasks to coding assistants (Codex, Claude Code, or Antigravity):

### 1. New Feature Implementation Prompt
```text
Implement [FEATURE NAME] in the MeetAI architecture.
First, review existing files and describe the implementation plan.
Then, make the minimal clean changes following our layered structure (app/api, app/services, app/repositories, app/schemas, app/models).
Include Pydantic validation, explicit error handling, and unit tests.
Do not rewrite unrelated files.
```

### 2. Architecture & Security Review Prompt
```text
Review the current MeetAI repository as a senior backend engineer.
Examine code organization, JWT security, database transaction safety, Celery idempotency, and error handling.
Return a structured list of Critical, High, and Medium issues with file links and recommended fixes.
```

### 3. Debugging Prompt
```text
Diagnose this failure: [DESCRIBE ERROR / PASTE LOGS].
Trace the request/event flow through the backend and database.
Identify the root cause without rewriting unrelated code.
Provide the minimal fix and add a regression test.
```

---

*Ready to build? Start with **Phase 0 (Day 1)** to bootstrap your backend, frontend, and Docker infrastructure!*
