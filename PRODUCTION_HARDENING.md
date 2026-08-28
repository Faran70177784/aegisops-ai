# AegisOps AI — Production Hardening

## Implemented baseline

- Production environment is explicitly enabled by Docker Compose.
- Debug mode is forced off in the production container.
- Production requires a strong JWT secret (32+ characters).
- Production rejects SQLite and expects PostgreSQL.
- Trusted Host middleware is enabled in production when `ALLOWED_HOSTS` is configured.
- Security headers middleware is enabled globally.
- GZip compression is enabled for larger responses.
- CORS is allow-list based rather than wildcard by default.
- API documentation can be disabled with `DOCS_ENABLED=false`.
- PostgreSQL uses a persistent Docker volume and a health check.
- Redis and Qdrant are isolated behind the `infra` Compose profile.
- Secrets are supplied through `.env` and are not committed to the repository.

## Production checklist

Before deployment:

1. Set a cryptographically random `JWT_SECRET_KEY` of at least 32 characters.
2. Set a strong unique `POSTGRES_PASSWORD`.
3. Set `ENVIRONMENT=production` and `DEBUG=false`.
4. Set `DOCS_ENABLED=false` unless protected API documentation is intentionally required.
5. Set `ALLOWED_HOSTS` to the real API hostnames only.
6. Set `CORS_ORIGINS` to the exact trusted frontend origins.
7. Configure the production PostgreSQL `DATABASE_URL`.
8. Configure the selected LLM provider and model.
9. Put TLS termination behind a trusted reverse proxy/load balancer.
10. Restrict PostgreSQL, Redis, and Qdrant to private network access.
11. Configure centralized logs, backups, monitoring, and alerting.
12. Run migrations before accepting application traffic.
13. Run the full test suite and a smoke test after deployment.

## Secrets

Never commit `.env`, database files, API keys, access tokens, or private certificates. Use a secret manager in cloud production.

## Docker deployment

```powershell
docker compose build --no-cache
docker compose up -d

docker compose exec api alembic upgrade head
docker compose ps
```

Verify the API:

```powershell
Invoke-WebRequest http://localhost:8000/health -UseBasicParsing |
    Select-Object StatusCode, Content
```

Expected response:

```text
200 {"status":"healthy"}
```

## Operational hardening still recommended for a public deployment

- TLS/HTTPS at the edge.
- Rate limiting at the reverse proxy/API gateway.
- Managed PostgreSQL with automated backups and point-in-time recovery.
- Centralized secret management.
- Container image vulnerability scanning.
- Dependency scanning and automated security updates.
- Metrics and distributed tracing.
- Log retention and alerting.
- Network policies/firewall rules.
- Regular credential rotation.
