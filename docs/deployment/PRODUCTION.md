# Production Deployment

## Required configuration

Set at minimum:

- `ENVIRONMENT=production`
- `DEBUG=false`
- `JWT_SECRET_KEY=<32+ random characters>`
- `DATABASE_URL=postgresql+psycopg2://...`
- `POSTGRES_PASSWORD=<strong password>`
- `ALLOWED_HOSTS=<deployed host names>`
- `CORS_ORIGINS=<trusted frontend origins>`

## Docker

```bash
docker compose up --build -d
```

The API container runs `alembic upgrade head` before starting Uvicorn.

## Production checklist

- Put TLS termination in front of the API.
- Restrict inbound database access to the application network.
- Store secrets in a secret manager or protected environment configuration.
- Back up PostgreSQL and test restoration.
- Centralize application and access logs.
- Monitor `/health` and container health status.
- Configure resource limits and horizontal scaling according to traffic.
- Do not use the demo seed passwords in a real deployment.
- Disable interactive API documentation if policy requires it by setting `DOCS_ENABLED=false`.
