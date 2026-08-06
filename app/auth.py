"""
auth.py
Login endpoint, password hashing, and JWT creation/verification.
Shared helper module — risk_engine.py calls create_access_token() once
a decision is "grant" or "step_up" passes MFA.
"""

import datetime
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.database import get_db
from app.models import LoginRequest, LoginResponse

SECRET_KEY = "dev-only-change-this-before-demo"  # move to env var before submission
ALGORITHM = "HS256"  # swap to RS256 with a real keypair if the report requires it
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def login(data: LoginRequest) -> LoginResponse:
    conn = get_db()
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (data.username,)
    ).fetchone()
    conn.close()

    if row is None or not verify_password(data.password, row["password_hash"]):
        return LoginResponse(status="fail")

    return LoginResponse(status="success", user_id=row["id"])
