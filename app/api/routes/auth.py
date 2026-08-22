from fastapi import APIRouter

from app.core.security import create_access_token
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(request: LoginRequest):

    token = create_access_token(
        request.user_id
    )

    return LoginResponse(
        access_token=token,
    )