from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from backend.app.api.rbac import require_permission
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.organization import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from backend.app.services.organization_service import OrganizationService
from backend.app.utils.audit import record_audit

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    data: OrganizationCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("organizations:create")),
) -> OrganizationResponse:
    organization = OrganizationService(db).create(data)
    record_audit(
        db, request, user_id=user.id, action="CREATE", resource_type="organization",
        resource_id=organization.id, description="Organization created.",
    )
    return OrganizationResponse.model_validate(organization)


@router.get("", response_model=list[OrganizationResponse])
def list_organizations(
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("organizations:read")),
) -> list[OrganizationResponse]:
    return [OrganizationResponse.model_validate(item) for item in OrganizationService(db).list()]


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("organizations:read")),
) -> OrganizationResponse:
    return OrganizationResponse.model_validate(OrganizationService(db).get(organization_id))


@router.patch("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    organization_id: int,
    data: OrganizationUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("organizations:update")),
) -> OrganizationResponse:
    organization = OrganizationService(db).update(organization_id, data)
    record_audit(
        db, request, user_id=user.id, action="UPDATE", resource_type="organization",
        resource_id=organization.id, description="Organization updated.",
        metadata_json={"fields": list(data.model_dump(exclude_unset=True).keys())},
    )
    return OrganizationResponse.model_validate(organization)


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    organization_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("organizations:delete")),
) -> None:
    OrganizationService(db).delete(organization_id)
    record_audit(
        db, request, user_id=user.id, action="DELETE", resource_type="organization",
        resource_id=organization_id, description="Organization deleted.",
    )
