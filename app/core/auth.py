from fastapi import Header, HTTPException

from app.core.security import decode_access_token


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> str:

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:

        user_id = decode_access_token(token)

    except ValueError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    return user_id