# Security Hardening

Implemented baseline:

- bcrypt password hashing.
- JWT expiration and issued-at claims.
- Production secret validation.
- Production debug prohibition.
- Production PostgreSQL requirement.
- HTTP security headers.
- Request IDs for traceability.
- Optional CORS allow-list.
- Optional Trusted Host allow-list.
- Generic internal error responses.
- RBAC on privileged APIs.
- Audit trail for authentication and privileged CRUD actions.
- Secret-safe audit metadata.
- Git ignore rules for `.env`, databases, credentials, logs, and virtual environments.

## Operational recommendations

For a full enterprise deployment, place the service behind a WAF/reverse proxy, use managed PostgreSQL, rotate JWT secrets through a controlled process, add centralized metrics/tracing, and enforce organizational retention and incident-response policies.
