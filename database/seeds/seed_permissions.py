from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.permission import Permission
from backend.app.models.role import Role


PERMISSIONS = [
    {
        "name": "organizations:read",
        "description": "View organizations.",
    },
    {
        "name": "organizations:create",
        "description": "Create organizations.",
    },
    {
        "name": "organizations:update",
        "description": "Update organizations.",
    },
    {
        "name": "organizations:delete",
        "description": "Delete organizations.",
    },
    {
        "name": "users:read",
        "description": "View users.",
    },
    {
        "name": "users:create",
        "description": "Create users.",
    },
    {
        "name": "users:update",
        "description": "Update users.",
    },
    {
        "name": "users:delete",
        "description": "Delete users.",
    },
    {
        "name": "dashboard:read",
        "description": "View dashboards.",
    },
    {
        "name": "reports:read",
        "description": "View reports.",
    },
    {
        "name": "analytics:read",
        "description": "View analytics and business insights.",
    },
]


ROLE_PERMISSIONS = {
    "admin": [
        "organizations:read",
        "organizations:create",
        "organizations:update",
        "organizations:delete",
        "users:read",
        "users:create",
        "users:update",
        "users:delete",
        "dashboard:read",
        "reports:read",
        "analytics:read",
    ],
    "executive": [
        "organizations:read",
        "users:read",
        "dashboard:read",
        "reports:read",
        "analytics:read",
    ],
    "manager": [
        "organizations:read",
        "users:read",
        "users:create",
        "users:update",
        "dashboard:read",
        "reports:read",
        "analytics:read",
    ],
    "analyst": [
        "organizations:read",
        "dashboard:read",
        "reports:read",
        "analytics:read",
    ],
}


def seed_permissions() -> None:
    db = SessionLocal()

    try:
        permissions_by_name: dict[str, Permission] = {}

        for permission_data in PERMISSIONS:
            permission = db.scalar(
                select(Permission).where(
                    Permission.name == permission_data["name"]
                )
            )

            if permission is None:
                permission = Permission(**permission_data)
                db.add(permission)
                db.flush()

                print(
                    f"Created permission: {permission.name}"
                )
            else:
                print(
                    f"Permission already exists: {permission.name}"
                )

            permissions_by_name[permission.name] = permission

        db.flush()

        for role_name, permission_names in ROLE_PERMISSIONS.items():
            role = db.scalar(
                select(Role).where(Role.name == role_name)
            )

            if role is None:
                raise RuntimeError(
                    f"Role does not exist: {role_name}. "
                    "Run seed_rbac.py first."
                )

            for permission_name in permission_names:
                permission = permissions_by_name[permission_name]

                if permission not in role.permissions:
                    role.permissions.append(permission)

                    print(
                        f"Assigned {permission_name} "
                        f"to role {role_name}"
                    )

        db.commit()

        print("Permission seeding completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_permissions()