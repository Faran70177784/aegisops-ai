from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.security import (
    create_access_token,
    verify_password,
)
from backend.app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def generate_user_token(user: User) -> str:
    return create_access_token(
        subject=str(user.id)
    )