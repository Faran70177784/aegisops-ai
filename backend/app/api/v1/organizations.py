from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.api.rbac import require_role
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from backend.app.services.organization_service import (
    OrganizationService,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> OrganizationResponse:
    service = OrganizationService(db)

    organization = service.create(data)

    return OrganizationResponse.model_validate(
        organization,
    )


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def list_organizations(
    db: Session = Depends(get_db),
    user: User = Depends(
        require_role(
            "admin",
            "executive",
            "manager",
            "analyst",
        ),
    ),
) -> list[OrganizationResponse]:
    service = OrganizationService(db)

    organizations = service.list()

    return [
        OrganizationResponse.model_validate(
            organization,
        )
        for organization in organizations
    ]


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(
        require_role(
            "admin",
            "executive",
            "manager",
            "analyst",
        ),
    ),
) -> OrganizationResponse:
    service = OrganizationService(db)

    organization = service.get(organization_id)

    return OrganizationResponse.model_validate(
        organization,
    )


@router.patch(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def update_organization(
    organization_id: int,
    data: OrganizationUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> OrganizationResponse:
    service = OrganizationService(db)

    organization = service.update(
        organization_id,
        data,
    )

    return OrganizationResponse.model_validate(
        organization,
    )


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> None:
    service = OrganizationService(db)

    service.delete(organization_id)