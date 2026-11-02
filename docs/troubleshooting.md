# Troubleshooting

- **PostgreSQL connection refused:** confirm PostgreSQL is running, the database exists, and the host/port in `DATABASE_URL` match your setup.
- **Alembic cannot find `app`:** run migration commands from `backend/` with its virtual environment active.
- **Vite cannot reach the API:** confirm the API is running on port 8000 and `VITE_API_URL` points to it.
- **npm install fails:** confirm registry access and supported Node/npm versions. A full dependency lockfile must be generated once package registry access is available.
- **Docker command not found:** install Docker Engine and its Compose plugin, or use the manual setup instructions.
- **Database migrations mismatch:** inspect `python -m alembic current` and `python -m alembic history`; back up before manually changing a shared database.
