# AegisOps AI Production Runbook

## 1. Configuration

Copy `.env.example` to `.env` and populate every production secret/configuration value.

Minimum security settings:

```env
ENVIRONMENT=production
DEBUG=false
DOCS_ENABLED=false
JWT_SECRET_KEY=<random-32-plus-character-secret>
POSTGRES_PASSWORD=<strong-password>
ALLOWED_HOSTS=<api-hostname>
CORS_ORIGINS=https://<trusted-frontend-host>
```

## 2. Build and start

```powershell
docker compose build --no-cache
docker compose up -d
```

## 3. Migration

```powershell
docker compose exec api alembic upgrade head
```

Confirm:

```powershell
docker compose exec api alembic current
docker compose exec api alembic heads
```

Both should report the same head revision.

## 4. Smoke test

```powershell
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing
Invoke-WebRequest http://localhost:8000/ -UseBasicParsing
```

## 5. Logs

```powershell
docker compose logs --tail=200 api
docker compose logs --tail=200 db
```

Look for startup errors, migration failures, database connection errors, and repeated 5xx responses.

## 6. Rollback

1. Stop application traffic.
2. Preserve logs and deployment metadata.
3. Restore the database if a destructive migration requires recovery.
4. Deploy the previously known-good image.
5. Re-run health and smoke tests.
6. Document the incident and corrective action.

Never delete the production database volume as part of an ordinary application rollback.
