from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from backend.app.api.rbac import require_permission
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserResponse, UserUpdate
from backend.app.services.user_service import UserService
from backend.app.utils.audit import record_audit

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("users:create")),
) -> UserResponse:
    created_user = UserService(db).create(data)
    db.commit()
    db.refresh(created_user)
    record_audit(
        db, request, user_id=user.id, action="CREATE", resource_type="user",
        resource_id=created_user.id, description="User created.",
        metadata_json={"role_id": created_user.role_id, "organization_id": created_user.organization_id},
    )
    return UserResponse.model_validate(created_user)


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("users:read")),
) -> list[UserResponse]:
    return [UserResponse.model_validate(item) for item in UserService(db).list()]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("users:read")),
) -> UserResponse:
    return UserResponse.model_validate(UserService(db).get(user_id))


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("users:update")),
) -> UserResponse:
    updated_user = UserService(db).update(user_id, data)
    db.commit()
    db.refresh(updated_user)
    record_audit(
        db, request, user_id=user.id, action="UPDATE", resource_type="user",
        resource_id=updated_user.id, description="User updated.",
        metadata_json={"fields": list(data.model_dump(exclude_unset=True).keys())},
    )
    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("users:delete")),
) -> None:
    UserService(db).delete(user_id)
    db.commit()
    record_audit(
        db, request, user_id=user.id, action="DELETE", resource_type="user",
        resource_id=user_id, description="User deleted.",
    )
