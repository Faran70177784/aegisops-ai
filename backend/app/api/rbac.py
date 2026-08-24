from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User


def require_role(*allowed_roles: str) -> Callable:
    def role_checker(
        user: User = Depends(get_current_user),
    ) -> User:
        if user.role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have an assigned role.",
            )

        if user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )

        return user

    return role_checker