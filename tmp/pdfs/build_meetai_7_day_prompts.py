from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "MeetAI_7-Day_Execution_Prompts.pdf"

NAVY = colors.HexColor("#10182B")
INK = colors.HexColor("#182238")
MUTED = colors.HexColor("#5F6B7A")
INDIGO = colors.HexColor("#4F46E5")
INDIGO_DARK = colors.HexColor("#3730A3")
TEAL = colors.HexColor("#0F9F8F")
AMBER = colors.HexColor("#F59E0B")
ROSE = colors.HexColor("#E85D75")
SKY = colors.HexColor("#2D8CFF")
PAPER = colors.HexColor("#F7F8FC")
PANEL = colors.HexColor("#EEF1FF")
LINE = colors.HexColor("#D9DEEA")
WHITE = colors.white

DAY_COLORS = [INDIGO, colors.HexColor("#6D5BD0"), SKY, TEAL, colors.HexColor("#D97706"), ROSE, INDIGO_DARK]


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Segoe", r"C:\Windows\Fonts\segoeui.ttf"))
    pdfmetrics.registerFont(TTFont("Segoe-Semibold", r"C:\Windows\Fonts\seguisb.ttf"))
    pdfmetrics.registerFont(TTFont("Segoe-Bold", r"C:\Windows\Fonts\segoeuib.ttf"))
    pdfmetrics.registerFont(TTFont("Consolas", r"C:\Windows\Fonts\consola.ttf"))


register_fonts()

base = getSampleStyleSheet()
styles = {
    "cover_kicker": ParagraphStyle(
        "cover_kicker", parent=base["Normal"], fontName="Segoe-Semibold", fontSize=10,
        leading=13, textColor=colors.HexColor("#B8C1FF"), spaceAfter=8, tracking=1.2,
    ),
    "cover_number": ParagraphStyle(
        "cover_number", parent=base["Normal"], fontName="Segoe-Bold", fontSize=88,
        leading=86, textColor=WHITE, alignment=TA_LEFT, spaceAfter=0,
    ),
    "cover_title": ParagraphStyle(
        "cover_title", parent=base["Title"], fontName="Segoe-Bold", fontSize=30,
        leading=35, textColor=WHITE, alignment=TA_LEFT, spaceAfter=12,
    ),
    "cover_subtitle": ParagraphStyle(
        "cover_subtitle", parent=base["Normal"], fontName="Segoe", fontSize=12,
        leading=18, textColor=colors.HexColor("#D9DDF8"), alignment=TA_LEFT,
    ),
    "h1": ParagraphStyle(
        "h1", parent=base["Heading1"], fontName="Segoe-Bold", fontSize=23,
        leading=29, textColor=NAVY, spaceAfter=8, keepWithNext=True,
    ),
    "h2": ParagraphStyle(
        "h2", parent=base["Heading2"], fontName="Segoe-Bold", fontSize=15,
        leading=20, textColor=NAVY, spaceBefore=8, spaceAfter=6, keepWithNext=True,
    ),
    "h3": ParagraphStyle(
        "h3", parent=base["Heading3"], fontName="Segoe-Semibold", fontSize=10.5,
        leading=14, textColor=INDIGO_DARK, spaceBefore=4, spaceAfter=3, keepWithNext=True,
    ),
    "body": ParagraphStyle(
        "body", parent=base["BodyText"], fontName="Segoe", fontSize=9.3,
        leading=13.4, textColor=INK, spaceAfter=6,
    ),
    "small": ParagraphStyle(
        "small", parent=base["BodyText"], fontName="Segoe", fontSize=8.1,
        leading=11.2, textColor=MUTED, spaceAfter=4,
    ),
    "bullet": ParagraphStyle(
        "bullet", parent=base["BodyText"], fontName="Segoe", fontSize=9,
        leading=12.6, textColor=INK, leftIndent=11, firstLineIndent=-8, spaceAfter=3,
    ),
    "day_kicker": ParagraphStyle(
        "day_kicker", parent=base["Normal"], fontName="Segoe-Semibold", fontSize=8.5,
        leading=11, textColor=INDIGO, tracking=1.1, spaceAfter=4,
    ),
    "day_title": ParagraphStyle(
        "day_title", parent=base["Heading1"], fontName="Segoe-Bold", fontSize=21,
        leading=25, textColor=NAVY, spaceAfter=4, keepWithNext=True,
    ),
    "day_subtitle": ParagraphStyle(
        "day_subtitle", parent=base["Normal"], fontName="Segoe", fontSize=9,
        leading=12, textColor=MUTED, spaceAfter=8, keepWithNext=True,
    ),
    "prompt_header": ParagraphStyle(
        "prompt_header", parent=base["Normal"], fontName="Segoe-Bold", fontSize=9,
        leading=12, textColor=WHITE, tracking=0.7,
    ),
    "prompt_label": ParagraphStyle(
        "prompt_label", parent=base["Normal"], fontName="Segoe-Semibold", fontSize=8,
        leading=10.5, textColor=INDIGO_DARK,
    ),
    "prompt_text": ParagraphStyle(
        "prompt_text", parent=base["BodyText"], fontName="Segoe", fontSize=8.35,
        leading=11.35, textColor=INK,
    ),
    "callout": ParagraphStyle(
        "callout", parent=base["BodyText"], fontName="Segoe-Semibold", fontSize=10,
        leading=14, textColor=NAVY,
    ),
    "table_head": ParagraphStyle(
        "table_head", parent=base["Normal"], fontName="Segoe-Bold", fontSize=8,
        leading=10, textColor=WHITE, alignment=TA_LEFT,
    ),
    "table_cell": ParagraphStyle(
        "table_cell", parent=base["BodyText"], fontName="Segoe", fontSize=7.8,
        leading=10.7, textColor=INK,
    ),
    "table_day": ParagraphStyle(
        "table_day", parent=base["Normal"], fontName="Segoe-Bold", fontSize=8.5,
        leading=11, textColor=INDIGO_DARK,
    ),
}


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet(text: str) -> Paragraph:
    return p(f"- {text}", "bullet")


def draw_cover(canvas, doc) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#1B2550"))
    canvas.circle(width - 35 * mm, height - 28 * mm, 49 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#293374"))
    canvas.circle(width - 12 * mm, 31 * mm, 54 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 7 * mm, height, fill=1, stroke=0)
    canvas.setTitle("MeetAI in 7 Days - Execution Prompts")
    canvas.setAuthor("MeetAI project planning synthesis")
    canvas.setSubject("Seven copy-ready prompts for completing the MeetAI platform")
    canvas.restoreState()


def draw_later_pages(canvas, doc) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 16 * mm, width, 16 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 16 * mm, 28 * mm, 2.2 * mm, fill=1, stroke=0)
    canvas.setFont("Segoe-Semibold", 7.5)
    canvas.setFillColor(colors.HexColor("#DDE2FF"))
    canvas.drawString(18 * mm, height - 10.3 * mm, "MEETAI / 7-DAY EXECUTION PROMPTS")
    canvas.setStrokeColor(LINE)
    canvas.line(17 * mm, 14 * mm, width - 17 * mm, 14 * mm)
    canvas.setFont("Segoe", 7.3)
    canvas.setFillColor(MUTED)
    canvas.drawString(17 * mm, 9 * mm, "Source synthesis: instruction.md + MeetAI_Detailed_Implementation_Guide.pdf")
    canvas.drawRightString(width - 17 * mm, 9 * mm, f"{doc.page}")
    canvas.restoreState()


def callout(text: str, accent=INDIGO) -> Table:
    table = Table([[p(text, "callout")]], colWidths=[172 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0F2FF")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D3D8F8")),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def prompt_table(rows: list[tuple[str, str]], accent) -> Table:
    data = [[p("COPY-READY DAILY PROMPT", "prompt_header"), ""]]
    data.extend([[p(label, "prompt_label"), p(text, "prompt_text")] for label, text in rows])
    table = Table(data, colWidths=[28 * mm, 144 * mm], repeatRows=1, splitByRow=1)
    style = [
        ("SPAN", (0, 0), (1, 0)),
        ("BACKGROUND", (0, 0), (1, 0), accent),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#E8EBFA")),
        ("BACKGROUND", (1, 1), (1, -1), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 1), (-1, -1), 0.45, LINE),
        ("BOX", (0, 0), (-1, -1), 0.7, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 5.2),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5.2),
    ]
    table.setStyle(TableStyle(style))
    return table


def add_day(story: list, number: int, title: str, source_days: str, mission: str, rows: list[tuple[str, str]]) -> None:
    accent = DAY_COLORS[number - 1]
    story.append(PageBreak())
    story.append(p(f"DAY {number} / SOURCE ROADMAP {source_days}", "day_kicker"))
    story.append(p(title, "day_title"))
    story.append(p("One standalone prompt. Paste it into the coding agent from the repository root.", "day_subtitle"))
    story.append(callout(mission, accent))
    story.append(Spacer(1, 5 * mm))
    story.append(prompt_table(rows, accent))


story: list = []

# Cover
story.append(Spacer(1, 30 * mm))
story.append(p("ACCELERATED BUILD PLAYBOOK", "cover_kicker"))
story.append(p("7", "cover_number"))
story.append(p("MeetAI in 7 Days", "cover_title"))
story.append(p("Seven high-level, copy-ready prompts to move an existing repository from foundation to a tested, deployed, portfolio-ready meeting intelligence platform.", "cover_subtitle"))
story.append(Spacer(1, 20 * mm))

cover_days = [[p(f"DAY {i}", "table_head")] for i in range(1, 8)]
day_strip = Table([sum(cover_days, [])], colWidths=[24 * mm] * 7)
day_strip.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#303B76")),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#6672BB")),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#6672BB")),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(day_strip)
story.append(Spacer(1, 22 * mm))
story.append(p("Designed from the complete instruction.md and all 9 pages of the MeetAI Detailed Project, Architecture & Implementation Guide.", "cover_subtitle"))
story.append(Spacer(1, 5 * mm))
story.append(p("Version 1.0  |  08 September 2026", "cover_kicker"))

# How to use
story.append(PageBreak())
story.append(p("How to use this playbook", "h1"))
story.append(callout("The source plan recommends 15 days at 4-6 focused hours per day. This seven-day version is an aggressive compression. Correctness, evidence and a working core outrank the calendar.", AMBER))
story.append(Spacer(1, 5 * mm))
story.append(p("Operating contract", "h2"))
for text in [
    "Run one prompt per day, in order. Each prompt is standalone but assumes the previous day's acceptance gate passed.",
    "Start from the repository root. Give the agent terminal access, the current codebase and the previous day's handoff report.",
    "Require inspection and a file-level plan before edits. Preserve working code, unrelated changes and user data.",
    "Do not advance past a failed dependency. Mark the day PARTIAL, carry the unfinished core forward and cut polish before cutting correctness.",
    "Make small, coherent commits only after relevant tests and runtime checks pass. Never force-push or erase uncommitted work.",
    "When Docker, an API key, certificates or a cloud target are unavailable, record the exact blocker. Do not substitute an unverified claim.",
]:
    story.append(bullet(text))

story.append(p("Rules repeated across all seven prompts", "h2"))
rules = [
    [p("Architecture", "table_day"), p("Routes parse HTTP and inject dependencies; services hold business logic; repositories own SQL; schemas use Pydantic; models use SQLAlchemy; WebSocket and worker logic stay in their dedicated layers.", "table_cell")],
    [p("Quality", "table_day"), p("Python is fully typed; TypeScript stays strict with no casual any; multi-table writes are atomic; every feature includes positive and negative tests.", "table_cell")],
    [p("Safety", "table_day"), p("No secrets in Git, no raw stack traces, no AI work in request handlers, no destructive migrations, no skipped tests and no fabricated metrics or success claims.", "table_cell")],
    [p("Scope", "table_day"), p("No WebRTC, calendar sync, enterprise RBAC/SSO, diarization, live AI assistant, vector/RAG search or analytics dashboard. Build uploaded-audio, OWNER/PARTICIPANT, timestamped transcript and PostgreSQL search flows.", "table_cell")],
]
rules_table = Table(rules, colWidths=[31 * mm, 141 * mm])
rules_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8EBFA")),
    ("BACKGROUND", (1, 0), (1, -1), WHITE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(rules_table)

# Map
story.append(PageBreak())
story.append(p("Seven-day dependency map", "h1"))
story.append(p("The compression groups adjacent source phases into complete vertical slices. Security and testing happen every day, then receive dedicated consolidation before release.", "body"))
map_rows = [[p("DAY", "table_head"), p("FOCUS", "table_head"), p("SOURCE DAYS", "table_head"), p("NON-NEGOTIABLE GATE", "table_head")]]
map_data = [
    ("1", "Foundation + data layer", "1-2", "Health, UI, Postgres/Redis and migration verified"),
    ("2", "Authentication + meetings", "3-4", "Two-user auth and authorization flows pass"),
    ("3", "Real-time collaboration", "5-7", "Persistent chat, presence and cross-worker delivery pass"),
    ("4", "Audio + AI pipeline", "8-10", "Upload reaches stored transcript and structured AI output"),
    ("5", "History, search + security", "11-12", "Authorized search and abuse controls pass"),
    ("6", "Tests + production deployment", "13-14", "Full test matrix and six-service stack pass"),
    ("7", "Release acceptance + portfolio", "15 + closure", "Deployed E2E evidence and honest metrics complete"),
]
for day, focus, source, gate in map_data:
    map_rows.append([p(day, "table_day"), p(focus, "table_cell"), p(source, "table_cell"), p(gate, "table_cell")])
map_table = Table(map_rows, colWidths=[16 * mm, 53 * mm, 25 * mm, 78 * mm], repeatRows=1)
map_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F2F4F9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(map_table)
story.append(Spacer(1, 6 * mm))
story.append(p("Critical path", "h2"))
story.append(callout("Foundation -> data model -> authentication -> meeting authorization -> WebSocket rooms -> audio job -> transcript -> summary -> search -> full tests -> deployment -> portfolio evidence", TEAL))
story.append(Spacer(1, 4 * mm))
story.append(p("Daily handoff rule", "h2"))
story.append(p("Every prompt ends with the same evidence package: status, changed files, architecture/data flow, exact commands and results, migration impact, security notes, residual risks, and the next day's prerequisites. A plain 'done' is not an acceptable handoff.", "body"))


# Source reconciliation
story.append(PageBreak())
story.append(p("Decisions to lock before implementation", "h1"))
story.append(p("The two source documents are aligned on architecture but leave a few implementation choices open. Day 1 should record these decisions once so later prompts do not create incompatible contracts.", "body"))
decision_rows = [[p("TOPIC", "table_head"), p("LOCKED DECISION", "table_head"), p("WHY IT MATTERS", "table_head")]]
decisions = [
    ("API paths", "Choose one canonical versioned REST prefix and preserve any compatibility aliases deliberately.", "The sources alternate among /api, /api/v1 and unversioned examples."),
    ("Database URL", "Use localhost for host-run tools and Docker service DNS (db) for container traffic; keep one database name.", "A host URL cannot connect from another container."),
    ("DB drivers", "Use asyncpg for the async application engine; keep the sync driver only for tools that require it.", "Mixed implicit engine modes create migration and worker surprises."),
    ("Completion", "Define COMPLETED as the entire required transcript plus intelligence transaction being durable, or add explicit stage states.", "The source roadmap can otherwise mark transcription complete too early."),
    ("Test evidence", "All selected tests must pass; report coverage as a separate measured percentage.", "An 80 percent pass rate is not a release-quality test gate."),
    ("WebSocket join", "Specify an authenticated join acknowledgement while retaining the documented event envelope and close code 4001.", "The event table defines a request but no positive acknowledgement."),
    ("Upload/provider", "Make format allowlist, size, storage, retention and provider model names environment-configurable and tested.", "Those details vary by environment and provider lifecycle."),
    ("Profile scope", "Include minimal profile read/update because profile management is a stated success criterion.", "The short roadmap mentions current-user retrieval but not update."),
]
for topic, decision, why in decisions:
    decision_rows.append([p(topic, "table_day"), p(decision, "table_cell"), p(why, "table_cell")])
decision_table = Table(decision_rows, colWidths=[29 * mm, 86 * mm, 57 * mm], repeatRows=1)
decision_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F2F4F9")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(decision_table)
story.append(Spacer(1, 6 * mm))
story.append(callout("Record these decisions in code, tests and README. Do not let different services or daily agents silently choose different contracts.", AMBER))


# Day 1
add_day(
    story, 1, "Foundation and complete data layer", "DAYS 1-2",
    "Turn the existing repository into a verified React/FastAPI/PostgreSQL/Redis foundation with the complete durable schema. Do not assume Phase 0 is finished, and do not silently use SQLite as proof of PostgreSQL readiness.",
    [
        ("ROLE", "You are the lead full-stack engineer inside the existing MeetAI repository. Complete Day 1 autonomously, but preserve working code and all unrelated user changes."),
        ("INSPECT FIRST", "Read repository instructions, inspect Git status, existing backend/frontend/config/migrations/tests, and run the current checks. Report the plan and exact files before editing. Reuse correct work instead of rescaffolding."),
        ("FOUNDATION", "Verify FastAPI with title <b>MeetAI API</b>, version <b>1.0.0</b>, restricted CORS, <font name='Consolas'>/health</font>, <font name='Consolas'>/api/health</font> and docs. Verify React + Vite + strict TypeScript + Tailwind + Router. Provide environment validation without exposing secrets. Compose must use PostgreSQL 16, Redis 7, persistent volumes and the single database name <font name='Consolas'>meetai_db</font>."),
        ("DATA LAYER", "Implement SQLAlchemy 2 models for users, refresh_tokens, meetings, meeting_participants, messages, transcripts, transcript_segments, meeting_summaries and action_items. Add typed enums, timestamps, foreign keys, uniqueness, indexes, cascades and relationships. Create matching Pydantic v2 schemas plus repository/service foundations without putting SQL in routes."),
        ("MIGRATIONS", "Wire Alembic metadata, create the initial meaningful revision, review generated SQL, and verify upgrade, downgrade and re-upgrade against PostgreSQL without deleting existing user data. Multi-model operations must be transaction-ready."),
        ("TEST + VERIFY", "Install dependencies in project-local environments. Run backend tests, import/compile checks, frontend production build, Compose validation, service health, migration checks and real HTTP requests. If Docker's Linux engine is unavailable, record the blocker and mark infrastructure PARTIAL; do not substitute SQLite."),
        ("ACCEPTANCE", "PASS only when health responses and docs load, Vite builds and serves, PostgreSQL and Redis are reachable, migration round-trip works, all nine tables have correct constraints, tests pass and no secret is tracked."),
        ("HANDOFF", "Return PASS/PARTIAL/FAIL, changed files, schema relationship summary, migration revision, exact commands/results, unresolved risks and Day 2 prerequisites. Commit only the verified Day 1 slice."),
    ],
)

# Day 2
add_day(
    story, 2, "Authentication and meeting lifecycle", "DAYS 3-4",
    "Deliver the first complete product slice: two users can authenticate, manage secure sessions, create or join meetings, and see authorized meeting data in the React application.",
    [
        ("ROLE", "Continue as the MeetAI lead engineer. Start from the verified Day 1 handoff. Do not redesign the data layer unless a demonstrated defect requires a migration."),
        ("INSPECT FIRST", "Review current models, schemas, repositories, services, routes, frontend auth state and tests. Trace the intended register -> login -> dashboard -> meeting flow, then present a scoped plan and file list."),
        ("AUTH", "Implement registration, strong password hashing, login, short-lived JWT access tokens, cryptographically random refresh tokens stored only as hashes, refresh rotation, revocation on logout, current-user/profile endpoints and inactive-user checks. Prevent token replay and never log credentials or tokens."),
        ("MEETINGS", "Implement create, list, detail, join, leave, cancel and archive operations with valid status transitions. Create the owner and OWNER participant atomically. Enforce OWNER/PARTICIPANT permissions on every resource; return clean 401/403/404 errors without leaking database details."),
        ("FRONTEND", "Build accessible Login, Register, protected routes, session restoration/refresh, logout, Dashboard lists/status badges, meeting creation/join flows and room navigation. Keep API types aligned with Pydantic responses and handle loading, empty and error states."),
        ("TEST + VERIFY", "Add service, repository, API and UI tests for happy paths and duplicate email, bad password, expired/invalid access, refresh rotation/reuse, revoked refresh, unauthorized access, invalid meeting transition and owner/participant boundaries. Run migrations, full backend tests, frontend tests/build and real API smoke flows with two users."),
        ("ACCEPTANCE", "PASS only when two users can register/login; refresh and logout behave securely; unauthorized calls return 401; forbidden meeting access returns 403; meeting lifecycle state is durable; the dashboard reflects correct accessible meetings; all tests pass."),
        ("HANDOFF", "Report status, changed files, access/refresh token data flow, meeting transaction and authorization rules, commands/results, remaining risks and the exact authenticated endpoints Day 3 will use. Commit only after verification."),
    ],
)

# Day 3
add_day(
    story, 3, "WebSockets, chat, presence and Redis reliability", "DAYS 5-7",
    "Create a reliable two-user meeting room with authenticated structured events, durable chat, live presence, Redis cross-worker delivery and reconnect behavior - without WebRTC.",
    [
        ("ROLE", "Implement the real-time collaboration vertical slice on top of the verified auth and meeting authorization layers. Preserve the REST contracts and database history."),
        ("INSPECT FIRST", "Trace WebSocket upgrade, token validation, meeting membership, room state, message persistence, Redis and frontend reconnect paths. Propose the event schemas and files before changing code."),
        ("PROTOCOL", "Use one typed envelope: <font name='Consolas'>{event, data, timestamp}</font>. Support connection.join, presence.joined, presence.left, chat.message, typing.start, typing.stop, meeting.state and controlled error. Authenticate at handshake or first join, authorize membership and close unauthorized sockets with code 4001."),
        ("SERVER", "Build room connection management, clean join/leave/disconnect handling, heartbeat ping/pong and stale cleanup. Persist chat to PostgreSQL before broadcast. Add bounded history retrieval. Integrate Redis Pub/Sub for multiple API workers, prevent self-echo/duplicate rebroadcast and clean subscriptions when rooms empty."),
        ("CLIENT", "Implement a typed WebSocket hook with exponential-backoff reconnect, token refresh coordination, resubscription/state recovery and deliberate retry limits. Build meeting room chat, history, participant presence, typing indicator, lifecycle state, accessibility and clear offline/error UI."),
        ("TEST + VERIFY", "Test valid/expired/unauthorized sockets, every event schema, persistence-before-broadcast, two clients, disconnect cleanup, heartbeat timeout, reconnect and Redis cross-worker delivery. Verify a page refresh reloads chat and a backend restart triggers recovery without duplicate messages."),
        ("ACCEPTANCE", "PASS only when two authorized sessions exchange ordered persistent messages, see accurate presence/typing/state, unauthorized users are rejected, multiple workers deliver once, reconnect recovers, all tests pass and no orphan room state remains."),
        ("HANDOFF", "Report status, event catalog, connection/message/Redis flow, exact multi-client and multi-worker evidence, changed files, commands/results, known scaling limits and Day 4 integration points. Commit the verified slice."),
    ],
)

# Day 4
add_day(
    story, 4, "Audio, Celery, transcription and AI intelligence", "DAYS 8-10",
    "Complete the asynchronous intelligence pipeline from an authorized audio upload to stored transcript segments, summary, decisions and action items rendered in the meeting UI.",
    [
        ("ROLE", "Implement the audio/AI pipeline as a durable background workflow. No transcription, transcoding or language-model call may execute inside a FastAPI request handler."),
        ("INSPECT FIRST", "Review transcript/summary models, storage settings, Celery configuration, Redis, OpenAI SDK usage, meeting permissions and frontend meeting view. Define the state machine and transaction boundaries before edits."),
        ("UPLOAD", "Add an authenticated meeting audio endpoint. Enforce participant authorization, configured size limit (25 MB unless configuration says otherwise), extension plus actual MIME/content checks for MP3/WAV and intentionally supported M4A, safe generated filenames, path traversal prevention and controlled errors. Persist UPLOADED before enqueueing."),
        ("WORKER", "Configure Celery/Redis and an idempotent task that atomically claims work, sets PROCESSING, calls the configured OpenAI transcription model with explicit timeout, and stores raw text plus ordered timestamp segments. Retry only transient failures with bounded exponential backoff; terminal failures set FAILED with sanitized diagnostics; clean temporary files."),
        ("INTELLIGENCE", "After transcription, request validated structured output for overview, key decisions and action items. Validate with Pydantic before atomic persistence. Re-delivery must replace or safely reuse results without duplicate segments, summaries or items. Set COMPLETED only after all required records commit."),
        ("FRONTEND", "Add upload/progress UI, polling or WebSocket state updates, retry guidance, timestamped transcript, summary, decisions and action-item views. Keep failed processing understandable without showing provider secrets or internal traces."),
        ("TEST + VERIFY", "Mock provider calls in automated tests. Cover invalid/oversize/unauthorized files, enqueue-after-commit, every state transition, transient retry, terminal failure, idempotent redelivery, atomic rollback and cleanup. Run a real-key smoke test only when a valid key is configured; otherwise label it unverified."),
        ("ACCEPTANCE", "PASS only when an allowed fixture follows UPLOADED -> PROCESSING -> COMPLETED and the UI renders stored transcript and structured output; rejection and FAILED/retry paths are proven; duplicate delivery is harmless; API remains responsive; all tests pass."),
        ("HANDOFF", "Report status, upload/job/provider/database/UI flow, state transition evidence, changed files, commands/results, mocked versus live verification, cost/privacy risks and Day 5 query contracts. Commit only verified work."),
    ],
)

# Day 5
add_day(
    story, 5, "History, PostgreSQL search and security hardening", "DAYS 11-12",
    "Make completed meeting intelligence discoverable only to authorized users, then harden every REST, WebSocket, file and background-job boundary before the full test and deployment day.",
    [
        ("ROLE", "Deliver authorized history/search and a repository-wide security/reliability hardening pass. Fix demonstrated issues with the smallest coherent changes and regression tests."),
        ("INSPECT FIRST", "Map access control from user -> participant -> meeting -> message/transcript/summary/action item. Audit API, WebSocket, storage, worker, logs, settings, dependency versions and existing tests. Rank findings Critical/High/Medium and plan before editing."),
        ("HISTORY + SEARCH", "Implement paginated meeting history and transcript inspection for accessible meetings only. Add PostgreSQL text search over meeting titles and transcript text/segments with appropriate indexes, bounded query/limit/offset or cursor rules, date/status filters and safe snippets/highlighting. Do not introduce embeddings, vector stores or RAG."),
        ("FRONTEND", "Build History and search views with filters, result context, transcript navigation, pagination, URL state, keyboard/accessibility support and loading, empty, error and forbidden states. Keep API types strict."),
        ("HARDEN", "Verify password/token hashing, expiry/rotation/revocation, resource checks everywhere, explicit production CORS, rate limits on register/login/upload/WebSocket, Pydantic input/output validation, file content/size/path safety, safe client errors/log redaction, secrets only in environment, atomic writes, provider timeouts/retries, job idempotency and pagination caps."),
        ("TEST + VERIFY", "Add authorization, injection-like input, pagination bounds, rate limit, CORS, upload abuse, path traversal, safe-error, retry and duplicate-job regression tests. Prove a spoken keyword returns only meetings visible to the caller and a nonparticipant receives 403. Run dependency and secret-hygiene checks without printing secrets."),
        ("ACCEPTANCE", "PASS only when history/search are correct, indexed, paginated and authorization-scoped; abuse controls work; errors reveal no internals; secrets are untracked; all new findings at Critical/High are resolved or explicitly block release; all tests/builds pass."),
        ("HANDOFF", "Report status, search query/index strategy, authorization matrix, findings and fixes, changed files, commands/results, unresolved Medium risks and the full Day 6 test/deployment prerequisites. Commit verified changes."),
    ],
)

# Day 6
add_day(
    story, 6, "Comprehensive testing and production deployment", "DAYS 13-14",
    "Convert daily confidence into release evidence, then package the six-service system behind Nginx with production-safe configuration and a repeatable deployment smoke test.",
    [
        ("ROLE", "Act as test lead and deployment engineer. Do not weaken assertions, skip failures or call a container configuration deployed until it has actually run in the available environment."),
        ("INSPECT FIRST", "Inventory the test matrix, coverage gaps, migration history, Dockerfiles, Compose, Nginx, health checks, environment contract and deployment target. Prioritize critical-path and failure-mode gaps, then list files and commands."),
        ("TEST MATRIX", "Complete unit tests for services/security/schemas; API tests for auth, meetings, audio and search including negative authorization; database tests for constraints/cascades/transactions and migration upgrade/rollback; WebSocket auth/events/disconnect/reconnect/cross-worker tests; Celery enqueue/retry/FAILED/idempotency tests with provider mocks; frontend component/integration tests; and the critical two-user E2E flow."),
        ("EVIDENCE", "Run every suite from a clean environment. All tests must pass. Measure and report actual coverage for core modules; target meaningful coverage around 80 percent or better when feasible, but never confuse a coverage target with test pass rate and never invent a number."),
        ("PRODUCTION", "Provide production builds and six services: frontend, backend, db, redis, celery_worker and nginx. Use health checks, persistent volumes, restart behavior, least-privilege/non-root containers where practical, a clear migration/startup strategy and production environment validation. Nginx must serve the app, proxy /api, upgrade /ws and terminate HTTPS using supplied certificates/configuration."),
        ("VERIFY", "Build from scratch, launch with one documented Compose command, wait for healthy status, inspect logs, run health and frontend smoke checks, verify WebSocket upgrade and execute the two-user critical flow through Nginx. Test migration behavior and service restart. If Docker/certs/cloud are unavailable, mark those checks PARTIAL rather than simulating success."),
        ("ACCEPTANCE", "PASS only when all test layers pass, production images build, all six services become healthy, Nginx routes HTTP/WebSocket correctly, HTTPS works on the deployment target, migrations are repeatable, no secret is baked or committed and the E2E critical path succeeds."),
        ("HANDOFF", "Report status, full command/result matrix, actual coverage, image/service health, deployment URL or precise blocker, changed files, rollback/restore notes, residual release risks and the Day 7 acceptance checklist. Commit only reproducible work."),
    ],
)

# Day 7
add_day(
    story, 7, "Final acceptance, resilience and portfolio readiness", "DAY 15 + CLOSURE",
    "Prove the deployed system end to end, fix release blockers, polish the user experience and produce honest portfolio evidence that can be explained in an interview.",
    [
        ("ROLE", "Act as release owner. Start from the deployed Day 6 handoff. Freeze feature scope: fix only release blockers, correctness defects, accessibility problems and documentation gaps."),
        ("ACCEPTANCE RUN", "Execute the deployed two-session journey: register/login -> create meeting -> second user joins -> presence/chat/typing -> refresh history -> upload allowed audio -> observe state transitions -> view transcript/summary/decisions/action items -> search a spoken keyword. Capture commands, logs and screenshots as evidence."),
        ("RESILIENCE", "Exercise unauthorized resource access, expired/revoked tokens, backend restart/reconnect, Redis/worker restart, duplicate task delivery, provider timeout and terminal AI failure -> FAILED -> controlled retry. Verify health endpoints, safe logs, data durability and clean recovery. Fix failures and add regression tests."),
        ("POLISH", "Refine responsive layouts, consistent visual hierarchy, keyboard navigation, focus states, contrast, loading/empty/error states and intentional dark/light behavior if already supported. Remove dead code and placeholders without destabilizing proven flows."),
        ("DOCUMENT", "Complete README/setup/deployment/migration/test/troubleshooting/limitations guidance. Add architecture, ERD and REST/WebSocket/job data-flow diagrams plus representative screenshots. Document security decisions, tradeoffs and scaling path. Keep future-scope exclusions explicit."),
        ("MEASURE", "Measure, never invent: representative API p95 latency, WebSocket event latency, tested concurrent participants, audio-to-COMPLETED duration, test coverage and any observed availability period. State environment, sample size and method; label unavailable metrics honestly."),
        ("INTERVIEW", "Produce a concise explanation of JWT/refresh rotation, meeting permissions, WebSocket room lifecycle, Redis roles, Celery/idempotency, transcript/summary schema, PostgreSQL search, Docker/Nginx and horizontal scaling. Ensure each statement matches implemented code."),
        ("ACCEPTANCE", "Return a final Definition of Done table with PASS/PARTIAL/FAIL and direct evidence for authentication, meetings, real-time, AI, search, security, testing, deployment, portfolio and understanding. Release only with no unresolved Critical/High defect, clean tests/builds, secret hygiene and a reproducible demo."),
        ("HANDOFF", "List changed files, final commit(s), exact verification commands/results, deployment/demo location, screenshots/metrics, known limitations and next safe improvements. After a clean release commit, synchronize requested branches only through fetched, ancestry-checked fast-forward updates or deliberate non-destructive merges; never force-push or overwrite divergence. Do not claim completion for unavailable external verification."),
    ],
)


# Final checklist
story.append(PageBreak())
story.append(p("Final definition of done", "h1"))
story.append(p("Use this after Day 7. Every PASS needs observable evidence; PARTIAL must name the missing verification and owner.", "body"))
dod_rows = [[p("AREA", "table_head"), p("DONE WHEN", "table_head"), p("EVIDENCE", "table_head")]]
dod_data = [
    ("Authentication", "Register, login, rotate refresh, logout, profile and authorization work.", "API tests + two-user smoke"),
    ("Meetings", "Create, join, leave, cancel, archive and history persist correctly.", "DB/API/UI evidence"),
    ("Real-time", "Two users chat and see presence with reconnect and cross-worker delivery.", "WS integration + live run"),
    ("AI pipeline", "Audio produces durable transcript, segments and structured intelligence.", "Worker tests + fixture run"),
    ("Search", "Authorized, paginated PostgreSQL search returns meeting/transcript matches.", "Query plan + API/UI tests"),
    ("Security", "Token, input, file, rate-limit, CORS, error and secret controls are proven.", "Negative tests + audit"),
    ("Testing", "All unit/API/DB/WS/worker/frontend/E2E tests pass; actual coverage reported.", "Clean test logs"),
    ("Deployment", "Six services run behind Nginx/HTTPS with health and restart checks.", "Compose status + smoke"),
    ("Portfolio", "README, diagrams, screenshots and measured metrics are accurate.", "Reviewed artifacts"),
    ("Understanding", "The owner can explain every major flow and tradeoff from the code.", "Interview walkthrough"),
]
for area, done, evidence in dod_data:
    dod_rows.append([p(area, "table_day"), p(done, "table_cell"), p(evidence, "table_cell")])
dod = Table(dod_rows, colWidths=[31 * mm, 102 * mm, 39 * mm], repeatRows=1)
dod.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F2F4F9")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(dod)
story.append(Spacer(1, 6 * mm))
story.append(callout("Release principle: the best portfolio version is not the one with the most code. It is the one that works, is tested, is deployed, is secure enough for its stated context, and can be explained clearly.", TEAL))


# Daily handoff template and exclusions
story.append(PageBreak())
story.append(p("Daily handoff template", "h1"))
story.append(p("Require the coding agent to end every day with this compact report. It makes the next prompt state-aware and prevents hidden carryover.", "body"))
handoff = [
    ("STATUS", "PASS / PARTIAL / FAIL, with one-sentence reason"),
    ("DELIVERED", "Implemented behavior and user-visible outcome"),
    ("FILES", "Created and modified files; migration revision if any"),
    ("DATA FLOW", "Request/event/job path and transaction boundaries"),
    ("VERIFICATION", "Exact commands, results, endpoints and runtime evidence"),
    ("SECURITY", "Authorization, secret, validation and failure-mode notes"),
    ("RISKS", "Known limitations, unverified external dependencies and follow-up"),
    ("NEXT DAY", "Contracts and prerequisites the next prompt can rely on"),
]
story.append(prompt_table(handoff, INDIGO))
story.append(Spacer(1, 6 * mm))
story.append(p("Scope lock", "h2"))
for text in [
    "Use uploaded audio, not native WebRTC streaming.",
    "Use in-app meeting scheduling, not Google or Outlook calendar sync.",
    "Use OWNER/PARTICIPANT roles, not enterprise multi-tenant RBAC or SSO.",
    "Use timestamped transcript segments, not speaker diarization.",
    "Use post-meeting intelligence, not a live AI meeting or voice assistant.",
    "Use PostgreSQL text search, not a vector database, embeddings or RAG.",
    "Measure real behavior; do not add an analytics dashboard or invent metrics.",
]:
    story.append(bullet(text))

story.append(Spacer(1, 5 * mm))
story.append(p("Source basis", "h2"))
story.append(p("This playbook synthesizes the complete repository instruction.md and all nine pages of MeetAI_Detailed_Implementation_Guide.pdf. It preserves the source architecture, success criteria, event protocol, data model, AI state machine, security checklist, test matrix, deployment target, scope exclusions and final definition of done while compressing the schedule from 15 days to seven.", "small"))


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=19 * mm,
    leftMargin=19 * mm,
    topMargin=23 * mm,
    bottomMargin=19 * mm,
    title="MeetAI in 7 Days - Execution Prompts",
    author="MeetAI project planning synthesis",
)
doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_later_pages)
print(OUTPUT)
