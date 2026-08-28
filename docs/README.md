# AegisOps AI Documentation

AegisOps AI is an enterprise operations platform built around FastAPI, PostgreSQL, RBAC, auditability, enterprise knowledge, RAG/search, AI services, workflows, automation, and analytics.

## Documentation map

- `architecture/ARCHITECTURE.md` — architecture overview
- `database/DATABASE.md` — database design and migrations
- `api/API.md` — API documentation
- `deployment/PRODUCTION.md` — deployment guidance
- `deployment/PRODUCTION_RUNBOOK.md` — operational deployment/runbook
- `deployment/SECURITY_HARDENING.md` — security hardening guidance

## Local verification

```powershell
docker compose up -d
docker compose exec api alembic upgrade head
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing
```
