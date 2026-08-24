from fastapi import APIRouter, Depends

from backend.app.api.rbac import require_role
from backend.app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


@router.get("/dashboard")
def admin_dashboard(
    user: User = Depends(
        require_role("admin"),
    ),
) -> dict[str, str]:
    return {
        "message": "Welcome to the administrator dashboard.",
        "user": user.email,
        "role": user.role.name,
    }