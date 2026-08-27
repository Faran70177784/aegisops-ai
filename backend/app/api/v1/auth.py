from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.schemas.user import UserResponse
from backend.app.services.auth_service import authenticate_user, generate_user_token
from backend.app.utils.audit import record_audit

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse, summary="Authenticate a user")
def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, request.email, request.password)

    if user is None:
        record_audit(
            db,
            http_request,
            user_id=None,
            action="LOGIN_FAILED",
            resource_type="authentication",
            description="Authentication attempt failed.",
            metadata_json={"reason": "invalid_credentials"},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = generate_user_token(user)
    record_audit(
        db,
        http_request,
        user_id=user.id,
        action="LOGIN",
        resource_type="authentication",
        description="User login recorded.",
    )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse, summary="Get the authenticated user")
def current_user(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)
