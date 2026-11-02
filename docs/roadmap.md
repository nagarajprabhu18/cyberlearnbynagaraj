# Development roadmap

Status is recorded against implemented and checked work; planned features are not described as complete.

| Phase | Scope | Exit evidence | Status |
|---|---|---|---|
| 1. Planning | Inspect workspace, define architecture, data model, boundaries, dependencies and delivery plan | Architecture and roadmap documents; environment baseline | Complete |
| 2. UI/UX | Design system, responsive landing page, reusable patterns, accessible motion | Build and UI tests; responsive review | In progress (responsive landing page and API-fed course catalog source built; npm packages unavailable offline) |
| 3. Backend | FastAPI, PostgreSQL, models/migrations, auth, courses, quizzes, admin | API tests, migration checks, authorization checks | In progress (schema, Argon2 registration/login, role checks, rate-limited auth, catalog, enrollment, progress and admin summary; quizzes/admin CRUD and recovery/verification flows remain) |
| 4. Integration | API client, protected routes, student dashboard, course player, quizzes and progress | End-to-end API/UI flows | Planned |
| 5. Advanced learning | Safe simulated labs, achievements, certificates, search, notifications, analytics | Feature-specific tests and safety review | Planned |
| 6. Quality | Unit/integration/browser, accessibility, responsive, security and error-path checks | CI green; findings resolved or documented | Planned |
| 7. Optimization | Performance, query, mobile and security-header review | Recorded profiling and header checks | Planned |
| 8. Documentation | Setup, Kali, database, configuration, API, testing, deployment, troubleshooting | Docs match verified behavior | Planned |
| 9. GitHub readiness | Ignore/secrets checks, CI, professional repository setup | Clean status, CI config, remote readiness | Planned |

## Delivery sequence

1. Establish a reproducible monorepo and design foundation.
2. Implement the vertical slice: registration/login, published course catalog, enrollment, lesson completion, and derived student progress.
3. Add quiz attempt persistence and feedback, then administration of course content.
4. Add safe simulated labs, achievement/certificate records, search, and notifications.
5. Harden and document deployment. Validate each slice before expanding scope.

## Initial dependency plan

- Frontend: React, TypeScript, Vite, Tailwind CSS, Framer Motion, Lucide React, Recharts, React Router, Vitest, Testing Library, Playwright.
- Backend: FastAPI, Pydantic, SQLAlchemy 2, Alembic, psycopg, Argon2 implementation, JWT/session support, rate limiting, pytest and HTTPX.
- Operations: PostgreSQL, Docker Compose, GitHub Actions.

Use supported stable releases pinned by lockfiles once package installation is available. Do not invent compatibility claims before resolving the dependency tree.

## Workspace inspection (2026-11-02)

The workspace contained no project source files, documentation, or usable Git repository metadata. The `.git` path exists as an empty directory, so repository history/remotes cannot be inspected. Python 3.13.12, Node.js 26.13.0, npm 11.20.0, Git 2.51.0, and PostgreSQL client 18.3 are present. Docker CLI is unavailable. No project code was overwritten.

## Current implementation checkpoint

Phase 1 documentation is complete. The landing page now reads published course content from the API, and the backend has an initial Alembic migration plus five passing API tests. Python compilation and Alembic schema drift checks pass. Frontend compilation and visual browser checks remain unverified because Vite/TypeScript packages are not installed and the package cache lacks required archives. Docker, PostgreSQL service integration, Git initialization, and GitHub push have not been verified.

## Risks and sequencing notes

- The complete requested scope is a substantial product; each feature must be implemented and checked in slices. A scaffold alone is not completion.
- Email delivery, production secret management, object storage, and TLS require deployment-specific providers and configuration.
- The present environment has no Docker CLI, and dependency/network availability is unverified.
- GitHub push requires authenticated access to the specified account and cannot be claimed until it is actually performed.
