from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_current_user
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.schemas.user import UserResponse
from backend.app.services.auth_service import (
    authenticate_user,
    generate_user_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db=Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(
        db,
        request.email,
        request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = generate_user_token(user)

    return TokenResponse(
        access_token=token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(user)