from sqlalchemy import select

from backend.app.core.security import hash_password
from backend.app.db.database import SessionLocal
from backend.app.models.role import Role
from backend.app.models.user import User


ADMIN_EMAIL = "admin@aegisops.ai"
ADMIN_NAME = "System Administrator"
ADMIN_PASSWORD = "Admin@12345"


def seed_admin() -> None:
    db = SessionLocal()

    try:
        admin_role = db.scalar(
            select(Role).where(Role.name == "admin")
        )

        if admin_role is None:
            raise RuntimeError(
                "Admin role does not exist. "
                "Run seed_rbac.py first."
            )

        existing_user = db.scalar(
            select(User).where(
                User.email == ADMIN_EMAIL
            )
        )

        if existing_user:
            print(
                f"Admin user already exists: {ADMIN_EMAIL}"
            )
            return

        admin_user = User(
            email=ADMIN_EMAIL,
            full_name=ADMIN_NAME,
            hashed_password=hash_password(
                ADMIN_PASSWORD
            ),
            is_active=True,
            role_id=admin_role.id,
        )

        db.add(admin_user)
        db.commit()

        print(
            f"Created admin user: {ADMIN_EMAIL}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()