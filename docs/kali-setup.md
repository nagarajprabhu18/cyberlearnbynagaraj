# Kali Linux setup

## Install tools

Install Python 3.13+, Node.js 22+, npm, PostgreSQL, and Git using your normal Kali package or version-manager workflow. Docker is optional if PostgreSQL is installed locally. Confirm versions with `python --version`, `node --version`, `npm --version`, `psql --version`, and `docker compose version`.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `DATABASE_URL` for your local PostgreSQL role/database. Generate `JWT_SECRET` with `python -c 'import secrets; print(secrets.token_urlsafe(48))'` and keep it only in the ignored `.env` file. Then run `python -m alembic upgrade head`, `python -m app.seed`, and `uvicorn app.main:app --reload`.

## Frontend

Open another terminal in the repository, run `cd frontend`, `npm install`, and `npm run dev`. Vite serves the UI on port 5173. Backend API docs are served on port 8000 in development.

## Safety

Lab exercises must remain simulations or use disposable, isolated local virtual machines that you are authorized to test. The application intentionally does not offer a server-side shell or arbitrary code runner.
