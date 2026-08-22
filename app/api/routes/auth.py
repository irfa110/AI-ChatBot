from fastapi import APIRouter, Depends, HTTPException

from app.core.security import create_access_token
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest
)

from sqlalchemy.orm import Session

from app.core.password import hash_password
from app.db.database import get_db
from app.db.models import User
from app.core.password import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.user_id == request.user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    valid_password = verify_password(
        request.password,
        user.password_hash,
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        user.user_id
    )

    return LoginResponse(
        access_token=token,
    )


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    existing_user = (
        db.query(User)
        .filter(
            User.user_id == request.user_id
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    user = User(
        user_id=request.user_id,
        password_hash=hash_password(
            request.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created successfully",
        "user_id": user.user_id,
    }