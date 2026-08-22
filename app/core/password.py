import bcrypt


MAX_PASSWORD_BYTES = 72


def _validate_password(password: str) -> bytes:

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > MAX_PASSWORD_BYTES:
        raise ValueError(
            "Password cannot be longer than 72 bytes"
        )

    return password_bytes


def hash_password(password: str) -> str:

    password_bytes = _validate_password(password)

    password_hash = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return password_hash.decode("utf-8")


def verify_password(
    password: str,
    password_hash: str,
) -> bool:

    password_bytes = _validate_password(password)

    return bcrypt.checkpw(
        password_bytes,
        password_hash.encode("utf-8"),
    )