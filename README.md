# AegisOps AI

AegisOps AI is an enterprise operations command-center foundation built around a versioned FastAPI backend, JWT authentication, role-based access control (RBAC), organization and user management, audit logging, and a production-oriented deployment baseline.

## Current release

**Version:** 1.0.0

### Completed work packages

| Phase | Status |
|---|---|
| Authentication & JWT | Complete |
| RBAC & permissions | Complete |
| Organization management | Complete |
| User management | Complete |
| Database migrations | Complete |
| Audit logging | Complete |
| Security hardening | Complete |
| API polish & documentation | Complete |
| Production / Docker | Complete |
| Final README | Complete |

## Architecture

```text
Client
  |
  v
FastAPI /api/v1
  |
  +-- Authentication / JWT
  +-- RBAC dependencies
  +-- Organizations API
  +-- Users API
  +-- Administration / Audit Logs
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
SQLAlchemy 2.x
  |
  +-- PostgreSQL (production)
  +-- SQLite (local development)
```

## Security baseline

- JWT access tokens with expiration and issued-at timestamps.
- Password hashing with bcrypt.
- RBAC enforcement at API boundaries.
- Production validation for JWT secret, debug mode, and database configuration.
- Security response headers and request IDs.
- Optional CORS and Trusted Host controls.
- Generic 401/403/500 responses without credential leakage.
- Audit events for authentication and privileged CRUD operations.
- Audit metadata intentionally excludes passwords and authentication tokens.
- Secrets are supplied through environment variables and `.env` is ignored by Git.

## Audit logging

The audit trail records:

- Successful and failed login attempts.
- Organization creation, updates, and deletion.
- User creation, updates, and deletion.
- Acting user ID when authenticated.
- Request IP address and User-Agent where available.
- Resource/action metadata useful for investigations.

Administrative endpoints:

- `GET /api/v1/admin/audit-logs`
- `GET /api/v1/admin/audit-logs/{audit_log_id}`

Audit-log access is restricted to the `admin` role.

## API

When documentation is enabled:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI schema: `/openapi.json`

Core endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Health check |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/me` | Current authenticated user |
| GET/POST | `/api/v1/organizations` | List/create organizations |
| GET/PATCH/DELETE | `/api/v1/organizations/{id}` | Read/update/delete organization |
| GET/POST | `/api/v1/users` | List/create users |
| GET/PATCH/DELETE | `/api/v1/users/{id}` | Read/update/delete user |
| GET | `/api/v1/admin/dashboard` | Admin dashboard |
| GET | `/api/v1/admin/audit-logs` | Audit-log search |
| GET | `/api/v1/admin/audit-logs/{id}` | Audit-log detail |

See `docs/api/API.md` for request examples and RBAC behavior.

## Local development

### 1. Create environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a local development configuration.

### 2. Create/update the database

```powershell
alembic upgrade head
```

### 3. Seed RBAC data

```powershell
python database/seeds/seed_rbac.py
python database/seeds/seed_permissions.py
python database/seeds/seed_admin.py
python database/seeds/seed_rbac_users.py
```

### 4. Run the API

```powershell
uvicorn backend.app.main:app --reload
```

### 5. Run tests

```powershell
python -m pytest tests -v
```

## Docker / production baseline

Production uses PostgreSQL and runs Alembic migrations before starting Uvicorn.

1. Copy `.env.example` to `.env`.
2. Set a strong `JWT_SECRET_KEY` (32+ random characters).
3. Set a strong `POSTGRES_PASSWORD`.
4. Configure `CORS_ORIGINS` and `ALLOWED_HOSTS` for the deployed domains.
5. Start the stack:

```bash
docker compose up --build -d
```

Optional Redis and Qdrant infrastructure is available through the `infra` profile:

```bash
docker compose --profile infra up --build -d
```

See `docs/deployment/PRODUCTION.md` for operational guidance.

## Database migrations

Current migration head:

`0906a1e85550_create_audit_logs`

Useful commands:

```powershell
alembic current
alembic check
alembic upgrade head
alembic downgrade -1
```

## Project structure

```text
AegisOps AI/
├── backend/app/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── rbac.py
│   │   └── v1/
│   ├── core/
│   ├── db/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── database/
│   ├── migrations/
│   └── seeds/
├── docs/
├── docker/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

## Engineering notes

The repository follows a layered architecture so API concerns, business logic, persistence, schemas, and security dependencies remain separated. Audit logging is implemented as a reusable service and is invoked by privileged application operations.

For production, use PostgreSQL rather than SQLite, keep secrets outside source control, terminate TLS at the deployment edge, configure a trusted host allow-list, and centralize logs/metrics in the infrastructure environment.

## License

See `LICENSE`.
