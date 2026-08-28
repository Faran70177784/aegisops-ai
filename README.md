# AegisOps AI

AegisOps AI is an enterprise operations command center designed around secure APIs, RBAC, auditability, PostgreSQL, enterprise knowledge, RAG/search, AI/LLM services, agents/workflows, automation, analytics, and an operational dashboard.

## Core stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL 16
- Docker Compose
- JWT authentication
- RBAC and audit logging
- Optional Redis and Qdrant infrastructure
- Ollama-compatible LLM configuration

## Repository areas

```text
backend/          FastAPI application
agents/           Agent/workflow foundation
rag/              Retrieval-augmented generation foundation
search/           Search infrastructure
knowledge_graph/  Knowledge graph foundation
evaluation/       Evaluation foundation
monitoring/       Monitoring foundation
tools/            Tooling foundation
database/         Migrations and seed scripts
tests/            Automated tests
docs/             Architecture, API, database and deployment documentation
docker/           Container entrypoint
```

## Local development

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure local values.

## Docker

```powershell
docker compose up -d
docker compose exec api alembic upgrade head
docker compose ps
```

Health check:

```powershell
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing
```

API documentation is available at `http://localhost:8000/docs` when `DOCS_ENABLED=true`.

## RBAC seed data

Run seeds from the project root inside the API container:

```powershell
docker compose exec api python -m database.seeds.seed_rbac
docker compose exec api python -m database.seeds.seed_permissions
docker compose exec api python -m database.seeds.seed_admin
docker compose exec api python -m database.seeds.seed_rbac_users
```

## Production

Read `PRODUCTION_HARDENING.md` and `docs/deployment/PRODUCTION_RUNBOOK.md` before deployment. Production must use PostgreSQL, a strong JWT secret, restricted hosts/CORS, secure secret management, TLS at the edge, backups, monitoring, and controlled migrations.

## Security

Do not commit `.env`, credentials, tokens, database files, private keys, or generated secrets. See `SECURITY.md` and `PRODUCTION_HARDENING.md`.
