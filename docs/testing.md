# Testing

## Backend

From `backend/`, activate the virtual environment and run `PYTHONPATH=. pytest -q`. Current API tests use an isolated in-memory SQLite database and the async HTTPX ASGI transport. They cover registration/login, student authorization, course enrollment/progress, and private response data.

## Frontend

From `frontend/`, install dependencies and run `npm test` for Vitest and `npm run build` for TypeScript/Vite production compilation. Playwright scenarios are planned but not yet implemented.

## Database migration

Run `python -m alembic upgrade head` against a disposable development database. To review schema changes, create a revision with `python -m alembic revision --autogenerate -m "describe change"`, inspect the generated file, then test upgrade and downgrade behavior before merging.

## Current limits

No frontend build, Vitest run, Playwright run, PostgreSQL integration run, accessibility scan, or security scan has been completed in the current restricted environment.
