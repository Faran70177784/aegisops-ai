from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.organization import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, organization_id: int) -> Organization | None:
        return self.db.get(Organization, organization_id)

    def get_by_name(self, name: str) -> Organization | None:
        statement = select(Organization).where(
            Organization.name == name,
        )

        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Organization | None:
        statement = select(Organization).where(
            Organization.slug == slug,
        )

        return self.db.scalar(statement)

    def list_all(self) -> list[Organization]:
        statement = select(Organization).order_by(
            Organization.id,
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        *,
        name: str,
        slug: str,
        description: str | None,
    ) -> Organization:
        organization = Organization(
            name=name,
            slug=slug,
            description=description,
        )

        self.db.add(organization)
        self.db.flush()
        self.db.refresh(organization)

        return organization

    def update(
        self,
        organization: Organization,
        values: dict,
    ) -> Organization:
        for field, value in values.items():
            setattr(organization, field, value)

        self.db.flush()
        self.db.refresh(organization)

        return organization

    def delete(self, organization: Organization) -> None:
        self.db.delete(organization)
        self.db.flush()