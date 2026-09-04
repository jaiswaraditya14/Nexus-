---
name: meetai
description: Comprehensive architecture, implementation guide, tech stack, data models, AI audio pipeline, WebSocket protocol, 15-day roadmap, and coding rules for the MeetAI platform.
---

# MeetAI: Project & Implementation Skill Guide

> **Project Reference**: Based strictly and exclusively on the `MeetAI_Detailed_Implementation_Guide.pdf` (15-Day Vibe-Coding Portfolio Build).
> **Primary Outcome**: A working, tested, containerized, and deployed real-time AI meeting platform.
> **Build Window**: 14–16 days (15-day recommended plan, 4–6 focused hours/day).
> **Core Principle**: Use AI to accelerate implementation, not to replace understanding. Every major subsystem must be explainable in a technical interview.

---

## 1. Purpose & Core Features

### 1.1 Project Purpose
MeetAI is a full-stack real-time meeting platform designed around authentication, meeting management, live communication, asynchronous audio processing, AI-generated meeting intelligence, searchable history, testing, and containerized deployment.

### 1.2 Core Success Criteria
* **Authentication**: Users can register, log in, refresh sessions, log out, and manage profiles.
* **Meeting Lifecycle**: Users can create, join, leave, cancel, and archive meetings.
* **Real-Time Collaboration**: Meeting participants can communicate in real time through WebSockets.
* **Chat & Activity Persistence**: Chat messages and meeting activity are persisted to PostgreSQL.
* **Asynchronous Audio Pipeline**: Audio files can be uploaded and processed asynchronously via Celery & Redis.
* **AI Intelligence**: Transcripts, segment-level timestamps, summaries, decisions, and action items are generated via OpenAI and persisted.
* **Search & History**: Meeting history, metadata, and transcript content are fully searchable with pagination.
* **Production Deployment**: Containerized with Docker Compose, reverse-proxied behind Nginx with HTTPS termination.
* **Testing & Quality**: Unit, API, database, WebSocket, Celery worker, and critical E2E flows are verified.

---

## 2. Technology Stack

| Layer | Technology | Architectural Role & Rationale |
| :--- | :--- | :--- |
| **Frontend Framework** | **React + TypeScript + Vite** | Component-based UI with strict type safety and fast HMR development. |
| **Styling** | **Tailwind CSS** | Rapid, consistent, responsive UI styling and dark/light design system. |
| **Routing** | **React Router** | Protected/authenticated page flows, meeting rooms, and navigation. |
| **Backend Framework** | **FastAPI (Python)** | High-performance, typed REST APIs, Pydantic validation, native WebSocket support. |
| **ORM** | **SQLAlchemy 2.x** | Modern type-annotated models, robust relational queries, and transaction management. |
| **Validation** | **Pydantic (v2)** | Request/response schemas, runtime validation, and structured data extraction. |
| **Database** | **PostgreSQL** | Durable relational data storage (users, meetings, transcripts, summaries, etc.). |
| **Database Migrations** | **Alembic** | Version-controlled, reproducible database schema migrations. |
| **Real-Time Communication** | **WebSockets** | Low-latency live meeting chat, presence updates, and room broadcast events. |
| **Cache & Broker** | **Redis** | High-speed broker for Celery queues and shared real-time pub/sub infrastructure. |
| **Background Workers** | **Celery** | Asynchronous task execution for long-running audio processing & AI calls. |
| **AI & LLM Services** | **OpenAI API** | Whisper for audio transcription; GPT models for structured meeting summaries, decisions, and action items. |
| **Containerization** | **Docker & Docker Compose** | Multi-container orchestration ensuring parity between local dev and production. |
| **Reverse Proxy / Ingress** | **Nginx** | Reverse proxy, static asset delivery, WebSocket proxying, and HTTPS/SSL termination. |
| **Testing Suite** | **Pytest + Frontend/E2E tooling** | Backend unit/API/DB/WebSocket/worker testing, and critical end-to-end integration tests. |

---

## 3. System Architecture & User Flow

### 3.1 High-Level Architecture Flow
```text
Internet 
   │
   ▼
[ Nginx (Reverse Proxy & Static Asset Server) ]
   ├───► Frontend (React / Vite Static Build)
   └───► Backend (FastAPI Application)
            │
            ├──────► PostgreSQL (Durable Application Data & State)
            │
            └──────► Redis (Celery Broker & Pub/Sub Infrastructure)
                        │
                        ▼
                 [ Celery Worker ]
                        │
                        ▼
                 [ OpenAI API ] (Whisper Transcription & Intelligence)
                        │
                        ▼
                 PostgreSQL (Persist Transcripts, Summaries, Action Items)
```

### 3.2 Backend & Frontend Separation
* **Backend Architecture**: Strictly organized into clean separation layers:
  * `app/api/`: REST route handlers and WebSocket endpoints.
  * `app/core/`: Configuration, security/JWT utilities, database engine setup, Celery app config.
  * `app/models/`: SQLAlchemy 2.x ORM entities.
  * `app/schemas/`: Pydantic request, response, and event schemas.
  * `app/services/`: Business logic layer (orchestrating jobs, processing rules).
  * `app/repositories/`: Database abstraction layer (data queries and persistence).
  * `app/websocket/`: Connection manager, room state, event routers.
  * `app/workers/`: Celery task definitions, audio handlers, OpenAI pipelines.
  * `tests/`: Automated unit, integration, and E2E test suites.
* **Frontend Architecture**:
  * `src/components/`: Shared reusable UI components.
  * `src/pages/`: Route-level pages (Login, Register, Dashboard, MeetingRoom, History).
  * `src/features/`: Domain-specific components and logic (chat, transcription viewer, audio uploader).
  * `src/hooks/`: Custom hooks (useAuth, useWebSocket, useMeeting).
  * `src/services/`: HTTP client API wrappers.
  * `src/types/`: TypeScript interfaces and type definitions matching backend schemas.

### 3.3 Primary User Journey
```text
Register ──► Login ──► Dashboard ──► Create / Join Meeting ──► Meeting Room
                                                                     │
  ┌──────────────────────────────────────────────────────────────────┘
  ▼
Real-time Chat / Presence ──► Audio Upload ──► Celery Processing ──► Transcript
                                                                          │
  ┌───────────────────────────────────────────────────────────────────────┘
  ▼
AI Summary / Action Items ──► Search / History Review
```

1. **Authentication**: User registers or logs in. FastAPI validates credentials and issues short-lived JWT access tokens and long-lived refresh tokens.
2. **Dashboard**: Authenticated user views upcoming and past meetings, access control, and creation controls.
3. **Meeting Creation**: User creates a meeting. FastAPI persists meeting and records owner/participant mapping.
4. **Joining & Handshake**: Participants join via meeting ID/slug, authenticate, and upgrade to a WebSocket connection.
5. **Live Meeting**: Real-time room events handle participant presence, live chat, typing indicators, and meeting lifecycle state.
6. **Audio Processing**: Recorded meeting audio is uploaded via authenticated REST API, validated (size, MIME type), and an `UPLOADED` record is created before queuing a background task.
7. **AI Pipeline**: Celery worker consumes the audio task, invokes OpenAI Whisper for transcription, persists transcript and segments, triggers AI analysis for structured summary and action items, and sets status to `COMPLETED`.
8. **Review & Action**: Participants review transcripts with segment timestamps, structured summaries, key decisions, and follow-up action items.
9. **Search**: Meeting metadata and full transcript content can be queried via paginated search endpoints.

---

## 4. WebSocket Communication Protocol

### 4.1 Two-User Communication Model
```text
[ User A Browser ] ──WebSocket──► [ FastAPI WebSocket Manager ] ──broadcast──► [ User B Browser ]
                                              │
                                              ├─► PostgreSQL (Persist chat.message)
                                              └─► Redis (Pub/sub for multi-worker scaling)
```

### 4.2 WebSocket Event Specification
All WebSocket payloads must follow a structured JSON schema:
```json
{
  "event": "<event_name>",
  "data": { ... },
  "timestamp": "ISO-8601-string"
}
```

| Event | Direction | Description & Payload Requirements |
| :--- | :--- | :--- |
| `connection.join` | Client → Server | Authenticate/connect user to a meeting room. Payload: `{ meeting_id: UUID, token: JWT }`. |
| `presence.joined` | Server → Room | Broadcast that a participant joined. Payload: `{ user_id: UUID, name: string, joined_at: string }`. |
| `presence.left` | Server → Room | Broadcast that a participant left. Payload: `{ user_id: UUID, name: string, left_at: string }`. |
| `chat.message` | Client → Server → Room | Send chat message; persisted to PostgreSQL before broadcast. Payload: `{ message_id: UUID, user_id: UUID, text: string, sent_at: string }`. |
| `typing.start` | Client → Room | Show typing indicator to other room members. Payload: `{ user_id: UUID, name: string }`. |
| `typing.stop` | Client → Room | Remove typing indicator for user. Payload: `{ user_id: UUID }`. |
| `meeting.state` | Server → Room | Synchronize meeting state changes (e.g. status changed to active, paused, archived). |
| `error` | Server → Client | Controlled error payload sent to the triggering client. Payload: `{ code: string, message: string }`. |

### 4.3 Reliability & Lifecycle Rules
* **Authentication**: Enforce token validation on initial WebSocket handshake or immediately upon `connection.join`. Disconnect unauthorized sockets with close code `4001` (Unauthorized).
* **Heartbeats**: Implement ping/pong keep-alive checks to identify dead connections.
* **Disconnect / Reconnect Handling**: Clean up participant presence on unexpected disconnects; clients must implement exponential backoff reconnection.
* **Redis Pub/Sub**: Use Redis to broadcast events across multiple FastAPI workers if running clustered instances.

---

## 5. Database Schema & Relational Design

### 5.1 Entity Relationship Diagram (Conceptual)
```text
  ┌──────────────┐          1:N           ┌───────────────────────┐
  │    users     ├───────────────────────►│     refresh_tokens    │
  └──────┬───────┘                        └───────────────────────┘
         │
         │ 1:N (owner)
         │                                M:N
         ▼                          ┌──────────────┐
  ┌──────────────┐ 1:N              │              │ N:1
  │   meetings   ├─────────────────►│   meeting_   ├──────┘
  └──────┬───────┘                  │ participants │
         │                          └──────────────┘
         ├───────────────┬────────────────────────────┐
         │ 1:N           │ 1:1                        │ 1:N
         ▼               ▼                            ▼
  ┌──────────────┐ ┌──────────────┐          ┌───────────────────────┐
  │   messages   │ │ transcripts  │          │   meeting_summaries   │
  └──────────────┘ └──────┬───────┘          └───────────┬───────────┘
                          │ 1:N                          │ 1:N
                          ▼                              ▼
                   ┌──────────────┐          ┌───────────────────────┐
                   │  transcript_ │          │     action_items      │
                   │   segments   │          └───────────────────────┘
                   └──────────────┘
```

### 5.2 Table Specifications

1. **`users`**
   * Primary key: `id` (UUID).
   * Fields: `email` (unique, indexed), `hashed_password`, `full_name`, `avatar_url`, `is_active`, `created_at`, `updated_at`.
   * Purpose: Application identity and credentials. Never store plaintext passwords.

2. **`refresh_tokens`**
   * Primary key: `id` (UUID).
   * Fields: `user_id` (FK -> `users.id`, cascade delete), `token_hash` (indexed), `expires_at`, `revoked`, `created_at`.
   * Purpose: Controlled refresh-token handling with revocation support.

3. **`meetings`**
   * Primary key: `id` (UUID).
   * Fields: `title`, `description`, `owner_id` (FK -> `users.id`), `status` (`SCHEDULED`, `ACTIVE`, `ENDED`, `CANCELLED`, `ARCHIVED`), `scheduled_start`, `scheduled_end`, `created_at`, `updated_at`.
   * Purpose: Meeting metadata, status, and ownership.

4. **`meeting_participants`**
   * Primary key: `id` (UUID) or composite (`meeting_id`, `user_id`).
   * Fields: `meeting_id` (FK -> `meetings.id`), `user_id` (FK -> `users.id`), `role` (`OWNER`, `PARTICIPANT`), `joined_at`, `left_at`.
   * Purpose: Many-to-many relationship tracking room membership and history.

5. **`messages`**
   * Primary key: `id` (UUID).
   * Fields: `meeting_id` (FK -> `meetings.id`, indexed), `user_id` (FK -> `users.id`), `content` (text), `created_at` (indexed).
   * Purpose: Durable storage for real-time chat messages.

6. **`transcripts`**
   * Primary key: `id` (UUID).
   * Fields: `meeting_id` (FK -> `meetings.id`, unique, indexed), `audio_file_path`, `processing_status` (`UPLOADED`, `PROCESSING`, `COMPLETED`, `FAILED`), `error_message`, `raw_text`, `duration_seconds`, `created_at`, `updated_at`.
   * Purpose: Transcript metadata and aggregate text output for a meeting.

7. **`transcript_segments`**
   * Primary key: `id` (UUID).
   * Fields: `transcript_id` (FK -> `transcripts.id`, cascade delete, indexed), `start_time` (float), `end_time` (float), `speaker_label` (nullable), `text` (text), `order_index` (int).
   * Purpose: Detailed timestamped subtitle/segment content for playback sync.

8. **`meeting_summaries`**
   * Primary key: `id` (UUID).
   * Fields: `meeting_id` (FK -> `meetings.id`, indexed), `overview` (text), `key_decisions` (JSONB / text array), `created_at`.
   * Purpose: Structured meeting intelligence and decisions extracted by LLM.

9. **`action_items`**
   * Primary key: `id` (UUID).
   * Fields: `summary_id` (FK -> `meeting_summaries.id`), `meeting_id` (FK -> `meetings.id`), `task_description` (text), `assignee_name` (nullable), `status` (`PENDING`, `COMPLETED`), `due_date` (nullable), `created_at`.
   * Purpose: Concrete actionable tasks generated from the meeting intelligence stage.

---

## 6. AI & Audio Processing Pipeline

### 6.1 End-to-End Pipeline Architecture
```text
Audio Upload (Client)
   │
   ▼
FastAPI Validation (MIME type: mp3/wav/m4a, file-size limits)
   │
   ▼
PostgreSQL (Create transcript record with status: UPLOADED)
   │
   ▼
Enqueue Background Job (Redis Broker)
   │
   ▼
Celery Worker picks up task
   ├── Updates status to PROCESSING in PostgreSQL
   ├── Invokes OpenAI Whisper API (or audio chunking if needed)
   ├── Parses response -> persists `transcripts` & `transcript_segments`
   ├── Invokes OpenAI GPT API for structured summary, decisions, and action items
   ├── Persists `meeting_summaries` and `action_items` in PostgreSQL
   └── Updates status to COMPLETED (or FAILED with error details on exception)
   │
   ▼
React Frontend polls or receives WebSocket event -> displays transcript & AI output
```

### 6.2 Processing State Model
| State | Definition & Handling |
| :--- | :--- |
| `UPLOADED` | File upload accepted and validated; database processing record initialized. |
| `PROCESSING` | Celery worker has dequeued the job and is actively transcribing/summarizing. |
| `COMPLETED` | Audio transcribed, segments mapped, summary and action items successfully committed. |
| `FAILED` | Job encountered an unrecoverable error; failure reason saved for diagnostics and retry. |

### 6.3 Asynchronous Execution Rules
* **Non-Blocking API**: Never run Whisper or LLM extraction in the FastAPI request-response thread.
* **Idempotency**: Prevent duplicate processing runs. If a task is requeued, ensure it does not duplicate segment rows or summary records (use database transactions and state checks).
* **Retry & Backoff**: Configure Celery task retry policies (e.g., max 3 retries with exponential backoff) for transient OpenAI rate-limit (`429`) or network timeouts.
* **File Cleanup**: Temporary audio chunks or cached uploads must be removed after successful persistence or failed terminal attempts.

---

## 7. Authentication & Authorization

* **Token Architecture**:
  * **Access Token**: Short-lived (e.g., 15 minutes), JWT format, signed using `HS256` or `RS256`. Contains `sub` (user ID) and expiration.
  * **Refresh Token**: Long-lived (e.g., 7 days), cryptographically secure random string stored hashed in `refresh_tokens` table.
* **Password Hashing**: Passwords hashed using `bcrypt` or `argon2`. Plaintext passwords must never touch logs or databases.
* **Resource Authorization**:
  * Verify user permissions at the API layer for all meeting operations (`meeting.owner_id == current_user.id` or user is an active participant in `meeting_participants`).
  * Deny access to transcripts, chat messages, and summaries to unauthorized users.
* **WebSocket Authentication**:
  * Validate token during connection handshake query parameters or `connection.join` initial message. Reject invalid or expired tokens immediately.

---

## 8. Docker, Nginx & Deployment Strategy

### 8.1 Production Service Set (`docker-compose.yml`)
1. `frontend`: Static production build served via Nginx (or built via Vite multi-stage Docker build).
2. `backend`: FastAPI app running with Uvicorn (`workers` count tuned for CPU cores).
3. `db`: PostgreSQL container with persistent named volume.
4. `redis`: Redis service for Celery broker and cache.
5. `celery_worker`: Celery worker process executing audio and AI processing jobs.
6. `nginx`: Ingress reverse proxy terminating HTTPS/SSL, routing `/api` to FastAPI, `/ws` to WebSocket endpoints, and root `/` to the React build.

### 8.2 Deployment Verification Checklist
1. Open deployed frontend URL over HTTPS; complete user registration and login.
2. Create a meeting in Session A; open an Incognito window/Session B, log in as second user, and join.
3. Verify two-way live chat messages, presence updates, and typing indicators.
4. Upload an allowed audio recording (e.g., MP3/WAV within size limit).
5. Watch processing status transition from `UPLOADED` -> `PROCESSING` -> `COMPLETED`.
6. Verify transcript segments, summary overview, key decisions, and action items render in the UI.
7. Perform search queries across meeting history and transcript text.
8. Verify health check endpoints (`/health`, `/api/health`) and verify no secrets are committed to Git.

---

## 9. Security & Reliability Checklist

* [ ] **Password Security**: Hash passwords with bcrypt/argon2; never log or store plaintext.
* [ ] **Token Management**: Use short-lived access tokens and revocable refresh tokens in the database.
* [ ] **API Authorization**: Enforce meeting and resource-level authorization checks on every endpoint.
* [ ] **Input & File Validation**: Validate all request payloads via Pydantic; enforce MIME types and strict file-size limits (e.g., 25MB).
* [ ] **CORS Configuration**: Restrict CORS origins deliberately; do not use `Allow-Origins: *` in production.
* [ ] **Rate Limiting**: Apply rate limits to authentication endpoints (`/login`, `/register`), audio upload, and WebSocket connections.
* [ ] **Secrets Hygiene**: Store all credentials (JWT secrets, DB URLs, OpenAI API keys) in `.env` / environment variables, never in source control.
* [ ] **Safe Errors**: Suppress raw tracebacks and internal database errors in client responses. Return clean HTTP exceptions.
* [ ] **Timeouts & Retries**: Wrap external AI API calls in explicit timeouts and exponential backoff.
* [ ] **Job Idempotency**: Make background Celery tasks idempotent to guard against message redelivery.
* [ ] **WebSocket Cleanup**: Clean up severed connections, stale rooms, and ping timeouts.
* [ ] **Database Transactions**: Wrap multi-step state changes (e.g., meeting creation + participant mapping) in atomic DB transactions.
* [ ] **Pagination**: Enforce limit/offset or cursor pagination on search and meeting history endpoints.

---

## 10. Comprehensive Testing Strategy

| Test Layer | Focus Areas & What to Test |
| :--- | :--- |
| **Unit Tests** | Service logic, authentication helpers, password hashing, Pydantic validation, schema serialization. |
| **API Tests** | Auth flows (`/register`, `/login`, `/refresh`), meeting CRUD, audio upload validation, permission rejection (`403 Forbidden`), error status codes. |
| **Database Tests** | SQLAlchemy models, foreign key cascades, unique constraints, transactional integrity, and Alembic migration rollbacks. |
| **WebSocket Tests** | Connection authentication, `connection.join`, `chat.message` broadcast, presence announcements, typing indicators, unauthorized rejection, clean disconnect. |
| **Background Jobs** | Celery task invocation, retry behavior, error capture (`FAILED` state), audio pipeline mocking, duplicate job idempotency. |
| **Frontend Tests** | Login/Register forms, dashboard lists, meeting room chat interface, transcript segment viewer, loading and error states. |
| **End-to-End (E2E)** | Full critical path: Register -> Login -> Create Meeting -> User 2 Joins -> Real-time Chat -> Upload Audio -> Celery Processing -> Transcript & Summary Display -> Search. |

---

## 11. 15-Day Implementation Roadmap

| Day | Deliverable | Definition of Done |
| :---: | :--- | :--- |
| **1** | **Foundation** | Repository scaffolding, React + FastAPI setup, PostgreSQL, Redis, Docker Compose, `.env` config, working health checks. |
| **2** | **Database** | SQLAlchemy 2.x models, relationships, Alembic migrations initialized, Pydantic schemas, and repository base layer. |
| **3** | **Authentication** | Register, login, refresh token rotation, logout, current user (`/me`), password hashing, and React protected routes. |
| **4** | **Meetings** | CRUD endpoints: create, list, detail, join, leave, cancel, archive; Dashboard UI with meeting listings and status badges. |
| **5** | **WebSocket Foundation** | Authenticated WebSocket endpoint, room connection manager, join/leave lifecycle, broadcast engine, and disconnect cleanup. |
| **6** | **Chat + Presence** | Real-time chat messaging, message persistence in PostgreSQL, typing indicators, and live participant presence list. |
| **7** | **Redis + Reliability** | Redis pub/sub integration for multi-worker WebSocket support, client reconnect handling with backoff, and state recovery. |
| **8** | **Audio + Celery** | Validated audio upload endpoint, storage handler, Celery worker setup, and initial `UPLOADED`/`PROCESSING` state management. |
| **9** | **Transcription** | Celery task calling OpenAI Whisper, transcript and segment persistence in DB, and frontend transcript display. |
| **10** | **AI Intelligence** | OpenAI LLM integration for structured meeting summaries, key decisions, and action items; UI cards for summary and tasks. |
| **11** | **History + Search** | Meeting history views, transcript inspection, and search endpoint querying meetings and transcript text with pagination. |
| **12** | **Security Hardening** | Auth audit, rate limiting, file validation checks, CORS configuration, error sanitization, and Celery idempotency checks. |
| **13** | **Testing** | Comprehensive test coverage: Pytest for backend unit/API/DB/WS/worker, frontend component tests, and critical path E2E flow. |
| **14** | **Deployment** | Multi-container production Docker Compose, Nginx reverse proxy, HTTPS configuration, environment variable audit, smoke tests. |
| **15** | **Portfolio Polish** | UI aesthetic polish, README documentation, architecture & database diagrams, screenshots, performance metrics, interview prep. |

---

## 12. Scope Control: Strict Guardrails

To complete the working system within the 15-day build, the following features are **explicitly out-of-scope** and must NOT be started until the core platform is stable and tested:

* ❌ **Native WebRTC video/audio streaming** (Use audio upload + processing; do not build live peer-to-peer WebRTC).
* ❌ **Google Calendar or Microsoft Outlook synchronization**.
* ❌ **Complex enterprise multi-tenant RBAC** (Simple OWNER/PARTICIPANT roles are sufficient).
* ❌ **Speaker diarization** (Raw transcript segments are sufficient).
* ❌ **Live in-meeting AI assistant / voice agent**.
* ❌ **Vector database / embedding-based RAG search** (PostgreSQL text search is the designated solution).
* ❌ **Advanced analytics dashboard**.
* ❌ **Enterprise SSO (SAML / Okta)**.

---

## 13. Recommended Repository Structure

```text
meetai/
├── backend/
│   ├── app/
│   │   ├── api/             # API routes (auth, meetings, audio, search) and WebSocket routers
│   │   ├── core/            # Config, security (JWT, hashing), database session, Celery instance
│   │   ├── models/          # SQLAlchemy ORM models (User, Meeting, Message, Transcript, etc.)
│   │   ├── schemas/         # Pydantic validation schemas for request/response/events
│   │   ├── services/        # Business logic operations (auth service, meeting service, AI service)
│   │   ├── repositories/    # Database query abstractions and data access objects
│   │   ├── websocket/       # WebSocket ConnectionManager, room tracking, and event broadcasters
│   │   └── workers/         # Celery tasks (audio transcription, summarization, cleanup)
│   ├── tests/               # Pytest suites (unit, api, db, websocket, worker)
│   ├── alembic/             # Alembic migration environment and version files
│   ├── alembic.ini          # Alembic configuration
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container definition
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI primitives (buttons, modals, inputs, badges)
│   │   ├── pages/           # Route views (Login, Register, Dashboard, MeetingRoom, History)
│   │   ├── features/        # Feature modules (chat, meeting-controls, transcript-view, summary-card)
│   │   ├── hooks/           # Custom React hooks (useAuth, useWebSocket, useMeeting)
│   │   ├── services/        # Axios/Fetch API client abstractions
│   │   └── types/           # TypeScript interfaces matching backend models & WebSocket events
│   ├── tests/               # Frontend component and integration tests
│   ├── package.json         # Node dependencies and scripts
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── Dockerfile           # Frontend build container definition
├── nginx/
│   └── nginx.conf           # Nginx reverse proxy configuration (HTTP, WebSocket, SSL)
├── docker-compose.yml       # Full stack container orchestration
├── .env.example             # Documented template of required environment variables
├── README.md                # Project documentation and setup instructions
└── docs/                    # Architectural diagrams and technical specs
```

---

## 14. Vibe-Coding Workflow & Multi-AI Collaboration

### 14.1 The 10-Step Development Loop
Do not try to build everything at once. Work strictly feature-by-feature using this cadence:
1. **Define**: YOU define the specific feature from the 15-day plan.
2. **Propose**: AI proposes an architectural implementation plan and file list.
3. **Implement**: AI implements one scoped feature following existing patterns.
4. **Run**: YOU execute the code locally and verify behavior.
5. **Diagnose**: AI diagnoses any failures or runtime errors.
6. **Test**: AI writes regression and integration tests for the feature.
7. **Architecture Audit**: Claude Code reviews architecture, security, and data consistency.
8. **Frontend / UX Polish**: Antigravity reviews UI, responsive styling, and user interaction.
9. **Understand**: YOU ensure you understand the code and can explain every design decision.
10. **Commit**: Git commit the completed feature before proceeding.

### 14.2 AI Agent Specializations
* **Codex**:
  * Feature implementation, unit/API tests, debugging, refactoring, and Git/terminal workflows.
  * Work in small, scoped changes; require test coverage for bug fixes.
  * Require Codex to explain modified files and data flow after each subsystem.
* **Claude Code**:
  * Repository-wide architectural review and multi-file refactoring.
  * Security and reliability audits before making large changes.
  * Mandate root-cause analysis before generating code modifications.
* **Antigravity**:
  * Frontend implementation, visual consistency, responsive design, and UX polish.
  * Run after backend functionality works so visual iterations do not destabilize core services.

### 14.3 Reusable Prompts

#### Feature Implementation Prompt
```text
Implement [FEATURE] in the existing MeetAI architecture. First inspect the relevant files and explain the implementation plan. Then make the smallest coherent set of changes. Follow the existing service/repository/schema patterns, add validation and error handling, and add tests. Do not rewrite unrelated files. After implementation, list changed files and explain the data flow.
```

#### Architecture Review Prompt
```text
Review the current MeetAI repository as a senior engineer. Check architecture, security, data consistency, error handling, scalability and maintainability. Do not change code yet. Return Critical/High/Medium issues with file references, why each matters and a recommended fix.
```

#### Debugging Prompt
```text
Diagnose this failure in the existing MeetAI implementation. Do not guess and do not rewrite the subsystem. Trace the request/event/job flow, identify the root cause, explain it, propose the minimal fix, then implement it and add a regression test.
```

#### Interview Preparation Prompt
```text
Based only on the current MeetAI codebase, generate 30 technical interview questions with concise model answers. Cover FastAPI, PostgreSQL, JWT, WebSockets, Redis, Celery, AI processing, Docker, security and deployment. Do not ask about features that are not actually implemented.
```

---

## 15. Portfolio Metrics & Technical Interview Preparation

### 15.1 Measurable Portfolio Metrics
Never fabricate performance numbers. Collect actual metrics from the running, tested system:
* **API p95 Latency**: Measured across representative endpoints (`POST /api/auth/login`, `GET /api/meetings/{id}`, `GET /api/search`).
* **WebSocket Message Latency**: Measured round-trip event delivery time under controlled load.
* **Concurrent Participants**: Maximum concurrent WebSocket connections tested with stable delivery.
* **AI Processing Pipeline Time**: End-to-end duration from audio upload trigger to finalized transcript and summary persistence.
* **Test Coverage**: Real percentage reported by `pytest --cov` and test runners.
* **Deployment Availability**: Uptime recorded during staging and testing periods.

### 15.2 Strong Elevator Explanation
> *"MeetAI is a React/FastAPI real-time meeting platform. REST APIs handle authentication and meeting management, WebSockets handle live communication, PostgreSQL stores durable application data, Redis supports background and real-time infrastructure, and Celery moves long-running audio/AI processing out of the API request path. The application is containerized with Docker and deployed behind Nginx."*

### 15.3 Core Interview Subsystems to Master
1. **JWT Access & Refresh Strategy**: Short-lived access token + hashed refresh token database table; revocation on logout.
2. **Meeting Authorization**: How FastAPI dependencies enforce ownership and participation checks.
3. **WebSocket Connection Lifecycle**: Handshake auth, in-memory room routing, heartbeat ping/pong, and multi-worker Redis pub/sub.
4. **Redis Role**: Celery broker queue management vs. real-time pub/sub event broadcasting.
5. **Asynchronous Audio/AI**: Why long-running processing is detached from the HTTP thread pool, and how state transitions (`UPLOADED` -> `PROCESSING` -> `COMPLETED`/`FAILED`) work.
6. **Task Idempotency & Fault Tolerance**: Retry logic, exponential backoff, and avoiding duplicate AI records.
7. **Database Schema Modeling**: Transcripts vs. segment-level timestamps; summary overview vs. structured action items.
8. **Container Communication & Ingress**: How Nginx routes `/api`, `/ws`, and static assets inside Docker network.
9. **Horizontal Scalability**: Stateless API workers, Celery worker scaling, Redis pub/sub for WebSocket sync, and database read replicas.

---

## 16. Actionable Coding Rules for AI Agents (Codex / Claude Code / Antigravity)

1. **Strict Scope Discipline**: Under NO circumstances implement WebRTC, Google/Outlook calendar sync, live AI voice bots, vector search, or enterprise SSO. Any prompt requesting these must be redirected to the core scope.
2. **No Monolithic Files**: Always enforce the architectural pattern:
   * REST endpoints belong in `app/api/`.
   * Business logic belongs in `app/services/`.
   * Database queries belong in `app/repositories/`.
   * Data validation belongs in `app/schemas/`.
   * ORM definitions belong in `app/models/`.
3. **Pydantic Validation Everywhere**: Every incoming payload and outgoing response must use explicit Pydantic schemas. Avoid raw dictionaries.
4. **Safe Transactions**: Multi-model writes must always be executed within atomic SQLAlchemy sessions.
5. **No Leaking Secrets or Stacks**: Never return raw database errors or third-party exception tracebacks to API clients. Use custom application exception handlers.
6. **Asynchronous Audio Isolation**: Never perform transcription, file transcoding, or OpenAI completions inside a FastAPI route handler. Always dispatch to Celery.
7. **Idempotent Background Jobs**: Every Celery worker task must check the current database status before executing to ensure repeated messages do not corrupt data.
8. **Type Safety Across the Stack**: Strict TypeScript on frontend (`strict: true`), Python type annotations (`mypy`-compliant) on backend.
9. **Testing Requirement**: Every new feature or bug fix must include corresponding unit and/or integration tests before it is considered complete.
