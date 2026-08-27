# Architecture

## Layers

1. **API** — FastAPI routers, authentication dependencies, RBAC dependencies.
2. **Services** — business rules and transaction orchestration.
3. **Repositories** — SQLAlchemy persistence operations.
4. **Models** — database entities and relationships.
5. **Schemas** — Pydantic request/response contracts.
6. **Core** — configuration, security, exceptions, logging.
7. **Middleware** — transport-level security headers and request IDs.

## Security boundary

Authentication establishes the current user from a signed JWT. RBAC dependencies enforce role/permission requirements before protected handlers execute.

## Audit boundary

Audit logging is a separate service/repository pair. API operations record the authenticated actor, action, resource, request context, and safe metadata. Passwords, tokens, and secrets are never placed in audit metadata.

## Deployment boundary

Development may use SQLite. Production uses PostgreSQL behind the application container. Migrations are applied before the API starts.
