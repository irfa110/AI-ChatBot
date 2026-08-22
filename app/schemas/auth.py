from pydantic import BaseModel, Field, field_validator


def validate_password_bytes(value: str) -> str:

    if len(value.encode("utf-8")) > 72:
        raise ValueError(
            "Password cannot be longer than 72 bytes"
        )

    return value


class RegisterRequest(BaseModel):

    user_id: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=100,
    )

    _validate_password = field_validator(
        "password"
    )(validate_password_bytes)


class LoginRequest(BaseModel):

    user_id: str

    password: str = Field(
        min_length=8,
        max_length=100,
    )

    _validate_password = field_validator(
        "password"
    )(validate_password_bytes)


class LoginResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"