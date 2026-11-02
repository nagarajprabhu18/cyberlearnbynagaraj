# Deployment and security operations

The supplied Docker Compose file is for local development only. A production deployment needs a TLS reverse proxy, built static frontend, multiple API workers where appropriate, managed PostgreSQL, secret management, monitoring, backups, and tested restore procedures.

## Required configuration

- `DATABASE_URL`: PostgreSQL psycopg connection string from a secret manager.
- `JWT_SECRET`: cryptographically random, at least 32 characters, never checked into Git.
- `FRONTEND_ORIGINS`: explicit HTTPS origins; do not use `*` with credentials.
- `API_ALLOWED_HOSTS`: explicit hostnames accepted by the API in production.
- `ENVIRONMENT=production`: hides interactive API docs and enforces strong secret validation.
- Database credentials, email provider secrets, and any future object storage keys: injected at runtime, never in the image or frontend bundle.

Run Alembic as a one-off deployment migration job before routing traffic. Back up PostgreSQL on a defined schedule, encrypt backups, limit access, monitor restore age, and practice restores. Enable HTTPS/HSTS at the proxy. Restrict database ingress and admin access. Review headers and CSP for the actual frontend hosting origin before release.

## Security work still required before production

Email verification and password recovery provider integration, refresh-token rotation/revocation, account recovery policy, audit events, operational rate-limit storage for multiple workers, production host allowlist, and end-to-end security review are not implemented. The current API is an educational development slice, not a production-ready auth service.
