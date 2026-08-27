# AegisOps AI API Guide

Base path: `/api/v1`

## Authentication

`POST /auth/login`

Request:

```json
{
  "email": "admin@aegisops.ai",
  "password": "Admin@12345"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Authenticated requests use:

```text
Authorization: Bearer <jwt>
```

## RBAC

| Role | Organization create | User create | User delete | Audit logs |
|---|---:|---:|---:|---:|
| admin | yes | yes | yes | yes |
| executive | no | no | no | no |
| manager | no | yes | no | no |
| analyst | no | no | no | no |

## Audit-log search

`GET /admin/audit-logs`

Query parameters:

- `user_id` — filter by actor.
- `action` — filter by action such as `LOGIN`, `CREATE`, `UPDATE`, `DELETE`.
- `resource_type` — filter by resource type.
- `resource_id` — filter by resource identifier.
- `limit` — 1–500; default 100.

Example:

```text
GET /api/v1/admin/audit-logs?action=LOGIN&limit=20
```

Response shape:

```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "action": "LOGIN",
      "resource_type": "authentication",
      "resource_id": null,
      "description": "User login recorded.",
      "ip_address": "127.0.0.1",
      "user_agent": "...",
      "metadata_json": null,
      "created_at": "2026-08-27T12:00:00+00:00"
    }
  ],
  "count": 1
}
```

## Error model

Validation failures use HTTP 422. Authentication failures use HTTP 401. Authorization failures use HTTP 403. Conflict conditions use HTTP 409. Missing resources use HTTP 404. Unexpected errors are returned as a generic HTTP 500 response.
