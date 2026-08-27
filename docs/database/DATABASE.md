# Database

## Tables

- `roles`
- `permissions`
- `role_permissions`
- `users`
- `organizations`
- `audit_logs`

## Migration chain

```text
94cfce8a1f75
      |
      v
016a737d7d30
      |
      v
ab161f931efe
      |
      v
0906a1e85550  <-- current head
```

## Audit log retention

Audit records should normally be retained according to the organization's security/compliance policy. For high-volume deployments, archive older records to durable storage rather than allowing the operational database to grow without bounds.
