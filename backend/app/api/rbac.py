from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User


def require_role(*allowed_roles: str) -> Callable:
    """
    Require the authenticated user to have one of the specified roles.
    """

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


def require_permission(permission_name: str) -> Callable:
    """
    Require the authenticated user to have a specific permission.
    """

    def permission_checker(
        user: User = Depends(get_current_user),
    ) -> User:
        if user.role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have an assigned role.",
            )

        has_permission = any(
            permission.name == permission_name
            for permission in user.role.permissions
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )

        return user

    return permission_checker