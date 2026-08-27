from sqlalchemy import select

from backend.app.core.security import hash_password
from backend.app.db.database import SessionLocal
from backend.app.models.role import Role
from backend.app.models.user import User


RBAC_USERS = [
    {
        "email": "executive@aegisops.ai",
        "full_name": "AegisOps Executive",
        "password": "Executive@12345",
        "role": "executive",
    },
    {
        "email": "manager@aegisops.ai",
        "full_name": "AegisOps Manager",
        "password": "Manager@12345",
        "role": "manager",
    },
]


def seed_rbac_users() -> None:
    db = SessionLocal()

    try:
        for user_data in RBAC_USERS:
            existing_user = db.scalar(
                select(User).where(
                    User.email == user_data["email"],
                )
            )

            if existing_user:
                print(
                    f"RBAC user already exists: "
                    f"{user_data['email']}"
                )
                continue

            role = db.scalar(
                select(Role).where(
                    Role.name == user_data["role"],
                )
            )

            if role is None:
                raise RuntimeError(
                    f"Role does not exist: "
                    f"{user_data['role']}. "
                    "Run seed_rbac.py first."
                )

            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=hash_password(
                    user_data["password"],
                ),
                is_active=True,
                role_id=role.id,
            )

            db.add(user)

            print(
                f"Created RBAC user: "
                f"{user_data['email']} "
                f"({user_data['role']})"
            )

        db.commit()
        print("RBAC user seeding completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_rbac_users()