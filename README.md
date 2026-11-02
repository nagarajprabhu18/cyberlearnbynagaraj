# CyberLearn

CyberLearn is an education-first learning platform for networking, Linux, Python, and defensive security. Practical content is limited to simulations and isolated, authorized local labs. The server does not execute learner submitted code or shell commands.

> The workspace began empty. The current build contains the first landing page and the initial FastAPI course/progress API; authentication email verification, password recovery, quizzes, course player, administration tools, and several requested learner features are still in development. Do not deploy this as a finished production service.

## Current implementation

- Responsive dark landing page and five learning category cards.
- FastAPI REST API with OpenAPI in development mode.
- Argon2id password hashing, short lived JWT access tokens, normalized student/admin role tables, and login/registration rate limits.
- Course discovery/search, enrollment, lesson completion, and activity-derived dashboard counts.
- PostgreSQL-ready SQLAlchemy schema, Alembic initial migration, and safe starter course content.
- Four API tests for registration/login, permissions, enrollment/progress, and response privacy.
- Docker Compose development configuration, CI workflow, and architecture/roadmap documentation.

## Requirements

- Python 3.13 or compatible supported Python release.
- Node.js 22+ and npm.
- PostgreSQL 16+ for local use, or Docker Engine with Compose plugin.
- Git for repository work.

The supplied environment had no Docker CLI and could not download missing npm packages from its offline cache. Those environment checks must be repeated once network/package access is available.

## Quick start with Docker Compose

```bash
cp .env.example .env
# Edit .env and replace POSTGRES_PASSWORD and JWT_SECRET with local random values.
docker compose up --build
```

Then open <http://localhost:5173>. The API is at <http://localhost:8000>; interactive docs are at <http://localhost:8000/docs> in development. Stop with `docker compose down`; preserve the database volume unless you intentionally want to delete local data.

## Kali Linux manual setup

See [the Kali setup guide](docs/kali-setup.md). In brief, create a Python virtual environment in `backend/`, install `requirements.txt`, copy `backend/.env.example` to `backend/.env`, and run Alembic migrations and the safe starter catalog. In a separate terminal, install and run the Vite app from `frontend/`.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

For manual PostgreSQL setup, set `DATABASE_URL` in `backend/.env` to a PostgreSQL psycopg URL, ensure the database/user exist, then run the migration command above. SQLite is the default development fallback and is not recommended for production.

## Development checks

```bash
cd backend
PYTHONPATH=. pytest -q
python -m alembic upgrade head
```

```bash
cd frontend
npm run build
npm test
```

Frontend checks require package installation first. See [testing guide](docs/testing.md) and [API notes](docs/api.md).

## Environment and deployment

Use `.env.example` as a template only. Never commit `.env` files. Production requires a generated JWT secret of at least 32 characters, HTTPS, a restricted CORS origin list, managed PostgreSQL with monitored backups and restore drills, a secret manager, and a migration job. The included Compose file is for local development, not production. See [deployment and security](docs/deployment.md).

## Project map

```text
frontend/                 React + TypeScript + Vite application
backend/app/              FastAPI routes, SQLAlchemy models, settings, seed data
backend/migrations/       Alembic migration environment and revisions
backend/tests/            API tests
docs/                     Architecture, roadmap, setup and operations
.github/workflows/ci.yml  Backend and frontend CI jobs
docker-compose.yml        Local PostgreSQL/API/frontend services
```

## Roadmap and gaps

See [docs/roadmap.md](docs/roadmap.md) for phase status. The requested feature set is not yet complete: verification/reset email flows, secure refresh sessions, CSRF strategy for cookie sessions, full quiz attempts, lesson player UI, admin content CRUD, uploads, certificates, achievements, notifications, analytics, browser tests, and production hardening remain open work.

## License and certification

No third-party certification is implied. Any future course completion certificate will be explicitly labeled as a CyberLearn educational certificate and will not represent Cisco, CEH, or another certification body.
