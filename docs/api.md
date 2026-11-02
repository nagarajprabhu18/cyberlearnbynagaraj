# API notes

The development API currently exposes OpenAPI at `/openapi.json` and Swagger UI at `/docs`. Production disables those endpoints by default.

Implemented endpoints under `/api/v1`:

- `POST /auth/register` — create a student account (minimum 12 character password).
- `POST /auth/login` — return a short lived bearer access token.
- `GET /auth/me` — authenticated profile summary.
- `GET /courses?q=&difficulty=&limit=&offset=` — published course catalog.
- `POST /courses/{id}/enroll` — enroll the current student.
- `POST /lessons/{id}/complete` — mark a lesson complete for an enrolled student.
- `GET /dashboard` — counts derived from the current user's persisted activity.
- `GET /admin/overview` — counts restricted to users with the admin role.

Protected endpoints accept `Authorization: Bearer <access token>`. Do not log or expose tokens. Error payloads use FastAPI's standard JSON error format. Pagination is bounded to 100 rows per request.
