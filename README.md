# Nexus — Real-Time AI Meeting Intelligence Platform

> **Transform your team meetings into actionable intelligence in real time.**  
> Built with FastAPI, React, TypeScript, WebSockets, Celery, Redis, and OpenAI.

---

## 🌟 Overview

**Nexus** is a full-stack, real-time meeting collaboration and intelligence platform designed to eliminate meeting fatigue and lost context. Nexus handles live meeting interactions with low-latency WebSockets, runs asynchronous background audio processing through Celery and Redis, transcribes meetings with OpenAI Whisper, and automatically synthesizes discussions into structured summaries, key decisions, and follow-up action items with OpenAI GPT-4o.

---

## 🚀 Key Features

* 🔐 **Secure Authentication**: JWT-based access and refresh token rotation with cryptographically secure session revocation.
* 📅 **Meeting Lifecycle**: Create, schedule, join, manage, and archive collaborative meeting rooms.
* ⚡ **Real-Time Collaboration**: Sub-100ms WebSocket chat, presence announcements, and live typing indicators.
* 🎙️ **Asynchronous Audio Pipeline**: Decoupled audio upload, validation, and background processing powered by Celery & Redis.
* 📝 **Timestamped Transcripts**: High-fidelity speech-to-text conversion via OpenAI Whisper with segment-level timestamps.
* 🧠 **AI Meeting Intelligence**: Automated extraction of meeting overviews, key decisions, and assigned action items using GPT-4o.
* 🔍 **Searchable History**: Paginated, full-text search across meeting records and historical transcript content.
* 🐳 **Containerized Deployment**: Ready-to-deploy multi-container architecture orchestrated with Docker Compose and reverse-proxied behind Nginx.

---

## 🏗️ Architecture Flow

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

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | **React 18 + TypeScript + Vite** | High-performance, type-safe single page application |
| **Styling** | **Tailwind CSS** | Responsive, modern design system |
| **Routing** | **React Router v6** | Client-side routing and protected navigation flows |
| **Backend** | **FastAPI (Python 3.11+)** | Asynchronous, typed REST APIs and native WebSockets |
| **ORM & Migrations** | **SQLAlchemy 2.x & Alembic** | Database models, schema migrations, and transaction safety |
| **Data Validation** | **Pydantic v2** | Request and response schema validation |
| **Database** | **PostgreSQL 16** | Durable relational storage for meetings, users, and AI outputs |
| **Cache & Broker** | **Redis 7** | Celery task queue broker and real-time pub/sub layer |
| **Task Queue** | **Celery** | Asynchronous background processing for long-running AI jobs |
| **AI Models** | **OpenAI Whisper & GPT-4o** | Speech-to-text transcription and structured intelligence extraction |
| **Ingress & Proxy** | **Nginx** | Reverse proxy, static asset delivery, and WebSocket proxying |
| **Containerization** | **Docker & Docker Compose** | Multi-service local and production orchestration |

---

## 📂 Repository Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             # REST endpoints and WebSocket routers
│   │   ├── core/            # App config, database session, security, and Celery setup
│   │   ├── models/          # SQLAlchemy 2.x ORM models
│   │   ├── schemas/         # Pydantic v2 validation schemas
│   │   ├── services/        # Business logic operations
│   │   ├── repositories/    # Database query abstraction layer
│   │   ├── websocket/       # ConnectionManager and real-time broadcasters
│   │   └── workers/         # Celery task definitions (Whisper + GPT pipelines)
│   ├── alembic/             # Database migration versions
│   ├── tests/               # Automated unit, API, DB, and WebSocket tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI primitives
│   │   ├── pages/           # Application views (Auth, Dashboard, Meeting Room, History)
│   │   ├── features/        # Real-time chat, transcription viewer, AI summary cards
│   │   ├── hooks/           # useAuth, useWebSocket, useMeeting custom hooks
│   │   └── services/        # API client and network handlers
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── nginx/
│   └── nginx.conf           # Reverse proxy configuration
├── docker-compose.yml       # Local development & production orchestration
├── instruction.md           # Step-by-step developer implementation guide
└── README.md
```

---

## 🚦 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/jaiswaraditya14/Nexus-.git
cd Nexus-
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your settings:
```bash
cp .env.example .env
```
Ensure you provide your `OPENAI_API_KEY` for AI features.

### 3. Start Database & Redis
Ensure Docker Desktop is running, then start the services:
```bash
docker compose up -d db redis
```

### 4. Setup & Start Backend
```bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 5. Start Celery Worker
In a new terminal (with venv activated):
```bash
cd backend
celery -A app.core.celery_app.celery worker --loglevel=info
```

### 6. Setup & Start Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```

Visit **`http://localhost:5173`** to access the web application!

---

## 🧪 Testing

Run backend tests using `pytest`:
```bash
cd backend
pytest -v
```

---

## 📖 Detailed Instructions

For the complete 15-day implementation roadmap, system architecture specs, and step-by-step feature guides, refer to [instruction.md](instruction.md).

---

## 👤 Author

* **Aditya Jaiswar** — [GitHub Profile](https://github.com/jaiswaraditya14)

---

## 📄 License

This project is licensed under the MIT License.
