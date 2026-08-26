from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.api.rbac import require_role
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from backend.app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> UserResponse:
    service = UserService(db)

    created_user = service.create(data)

    return UserResponse.model_validate(created_user)


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    user: User = Depends(
        require_role(
            "admin",
            "executive",
            "manager",
            "analyst",
        ),
    ),
) -> list[UserResponse]:
    service = UserService(db)

    users = service.list()

    return [
        UserResponse.model_validate(item)
        for item in users
    ]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(
        require_role(
            "admin",
            "executive",
            "manager",
            "analyst",
        ),
    ),
) -> UserResponse:
    service = UserService(db)

    target_user = service.get(user_id)

    return UserResponse.model_validate(target_user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> UserResponse:
    service = UserService(db)

    updated_user = service.update(
        user_id,
        data,
    )

    return UserResponse.model_validate(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> None:
    service = UserService(db)

    service.delete(user_id)
