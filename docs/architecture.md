# CyberLearn architecture

## Product boundary

CyberLearn is a defensive, education-first platform. Hands-on activities are authored simulations or run in explicitly isolated local labs. The application server never executes learner-submitted commands or code. All analytics shown to students must be derived from persisted user activity; sample content and testimonials are labeled as examples.

## System shape

```text
Browser (React + TypeScript)
  └─ JSON REST API (FastAPI, /api/v1)
       └─ SQLAlchemy 2 + Alembic
            └─ PostgreSQL
```

The Vite frontend is a separately deployable static client. FastAPI owns authentication, authorization, validation, content delivery, progress, quizzes, and administration. PostgreSQL is the source of truth. Docker Compose provides local development services. Secrets enter through environment variables and are never committed.

## Monorepo boundaries

- `frontend/`: Vite, React, TypeScript, Tailwind, Framer Motion, Lucide, Recharts; feature-oriented components and API client.
- `backend/`: FastAPI application, Pydantic schemas, SQLAlchemy models/repositories, services, API routers, Alembic migrations.
- `tests/`: cross-service and browser scenarios; package-local unit tests remain near their code.
- `docs/`: architecture, roadmap, local setup, security, deployment and operations.
- `scripts/`: repeatable development and maintenance commands.

## Data model

Core entities: users, roles, categories, courses, lessons, enrollments, lesson progress, quizzes, questions, question options, quiz attempts/answers, achievements/user achievements, certificates, bookmarks, notes, and notifications. User-role and course-category relationships are normalized. Content references use foreign keys; user scoped records have uniqueness constraints (for example one progress row per user/lesson), indexed lookup columns, and UTC timestamps. Alembic is the only schema evolution path.

## Security decisions

- Passwords use Argon2id hashes. Authentication uses short-lived access tokens and rotating, HttpOnly, Secure, SameSite refresh cookies; production origins are explicitly configured. CSRF protection applies to cookie-authenticated mutations.
- Authorization is enforced in backend dependencies and service/query scope, with least-privilege student/admin roles. Never trust a role supplied by the client.
- Pydantic validates request and response boundaries; SQLAlchemy parameterizes queries. Render learner content as text/Markdown with raw HTML disabled. Avoid unsafe HTML injection.
- Rate limit registration, login, reset, and verification endpoints. Return generic authentication errors; redact secrets and tokens from logs.
- Uploads, when introduced, require size/type limits, generated names, storage outside the web root, and malware scanning. No arbitrary execution or shell access is provided.
- Set CSP, HSTS (TLS deployments), frame, MIME sniffing, and referrer headers at the serving edge/API. Keep CORS allowlists narrow.
- Email verification and reset are provider interfaces; development uses logged opaque links only when explicitly enabled, never password-bearing links.

## API conventions

Versioned REST endpoints under `/api/v1`; OpenAPI is generated from FastAPI schemas. List endpoints use bounded `limit`/`offset` pagination and validated filters. Mutations use transactions. Responses omit hashes, private tokens, and internal secrets. Health/readiness endpoints disclose no configuration details.

## Deployment shape

Local: frontend dev server + API + PostgreSQL via Compose. Production: TLS-terminating reverse proxy, built static frontend, API workers, managed PostgreSQL with backups and tested restore, secret manager, monitoring, and migration job. Compose is for local development, not a hardened production deployment.
