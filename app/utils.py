from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from config import security_config


def generate_access_token(data: dict[str, str | int], expiry: timedelta = timedelta(days=1)) -> str | None:
    try:
        return jwt.encode(
            payload={
                **data,
                "jti": str(uuid4()),
                "exp": datetime.now(timezone.utc) + expiry
            },
            algorithm=security_config.JWT_ALGORITHM,
            key=security_config.JWT_SECRET
        )
    except jwt.PyJWTError:
        return None

def decode_access_token(token: str) -> dict[str, str | int] | None:
    try:
        return jwt.decode(
                jwt=token,
                key=security_config.JWT_SECRET,
                algorithms=[security_config.JWT_ALGORITHM],
                )
    except jwt.PyJWTError:
        return None