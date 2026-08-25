from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.models.organization import Organization
from backend.app.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
)


class OrganizationService:
    def __init__(self, db: Session):
        self.repository = OrganizationRepository(db)
        self.db = db

    def create(
        self,
        data: OrganizationCreate,
    ) -> Organization:
        if self.repository.get_by_name(data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization name already exists.",
            )

        if self.repository.get_by_slug(data.slug):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization slug already exists.",
            )

        try:
            organization = self.repository.create(
                name=data.name,
                slug=data.slug,
                description=data.description,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization already exists.",
            )

    def get(self, organization_id: int) -> Organization:
        organization = self.repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        return organization

    def list(self) -> list[Organization]:
        return self.repository.list_all()

    def update(
        self,
        organization_id: int,
        data: OrganizationUpdate,
    ) -> Organization:
        organization = self.get(organization_id)

        values = data.model_dump(
            exclude_unset=True,
        )

        if "name" in values:
            existing = self.repository.get_by_name(
                values["name"],
            )

            if existing and existing.id != organization.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Organization name already exists.",
                )

        if "slug" in values:
            existing = self.repository.get_by_slug(
                values["slug"],
            )

            if existing and existing.id != organization.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Organization slug already exists.",
                )

        try:
            organization = self.repository.update(
                organization,
                values,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization update conflicts with existing data.",
            )

    def delete(self, organization_id: int) -> None:
        organization = self.get(organization_id)

        self.repository.delete(organization)

        try:
            self.db.commit()

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Organization cannot be deleted because it is "
                    "referenced by other records."
                ),
            )