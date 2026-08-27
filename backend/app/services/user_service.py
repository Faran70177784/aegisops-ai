from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import hash_password
from backend.app.models.organization import Organization
from backend.app.models.role import Role
from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UserRepository(db)

    def create(self, data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(data.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )

        role = self.db.get(Role, data.role_id)

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found.",
            )

        if data.organization_id is not None:
            organization = self.db.get(
                Organization,
                data.organization_id,
            )

            if organization is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Organization not found.",
                )

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            role_id=data.role_id,
            organization_id=data.organization_id,
            is_active=True,
        )

        return self.repository.create(user)

    def list(self) -> list[User]:
        return self.repository.list()

    def get(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return user

    def update(
        self,
        user_id: int,
        data: UserUpdate,
    ) -> User:
        user = self.get(user_id)

        if data.email is not None and data.email != user.email:
            existing_user = self.repository.get_by_email(data.email)

            if existing_user is not None and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists.",
                )

            user.email = data.email

        if data.full_name is not None:
            user.full_name = data.full_name

        if data.role_id is not None:
            role = self.db.get(Role, data.role_id)

            if role is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Role not found.",
                )

            user.role_id = data.role_id

        if data.organization_id is not None:
            organization = self.db.get(
                Organization,
                data.organization_id,
            )

            if organization is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Organization not found.",
                )

            user.organization_id = data.organization_id

        if data.is_active is not None:
            user.is_active = data.is_active

        return self.repository.update(user)

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)

        self.repository.delete(user)