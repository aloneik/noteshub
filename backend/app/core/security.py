from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_ALGORITHM = "HS256"


def get_password_hash(password: str | bytes) -> str:
    # Ensure password doesn't exceed bcrypt's 72-byte limit
    if isinstance(password, str):
        password_bytes = password.encode("utf-8")[:72]
        password = password_bytes.decode("utf-8", errors="ignore")
    elif isinstance(password, bytes):
        password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str | bytes, password_hash: str) -> bool:
    # Ensure password doesn't exceed bcrypt's 72-byte limit
    if isinstance(plain_password, str):
        password_bytes = plain_password.encode("utf-8")[:72]
        plain_password = password_bytes.decode("utf-8", errors="ignore")
    elif isinstance(plain_password, bytes):
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(
    *, subject: str, secret_key: str, expires_minutes: int = 60
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    to_encode = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(to_encode, secret_key, algorithm=JWT_ALGORITHM)


def decode_token(token: str, *, secret_key: str) -> Optional[dict]:
    try:
        return jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None
