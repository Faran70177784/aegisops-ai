from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.role import Role


ROLES = [
    {
        "name": "admin",
        "description": "Full system administration access.",
    },
    {
        "name": "executive",
        "description": "Executive dashboards, reports, and business insights.",
    },
    {
        "name": "manager",
        "description": "Operational management and authorized workflows.",
    },
    {
        "name": "analyst",
        "description": "Data analysis, enterprise search, and reporting.",
    },
]


def seed_roles() -> None:
    db = SessionLocal()

    try:
        for role_data in ROLES:
            existing_role = db.scalar(
                select(Role).where(
                    Role.name == role_data["name"]
                )
            )

            if existing_role:
                print(
                    f"Role already exists: {role_data['name']}"
                )
                continue

            role = Role(**role_data)
            db.add(role)

            print(
                f"Created role: {role_data['name']}"
            )

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()