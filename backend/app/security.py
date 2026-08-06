import datetime
from typing import Optional
import jwt
from passlib.context import CryptContext
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate an in-memory RS256 key pair for development
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PRIVATE_KEY_PEM = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)
PUBLIC_KEY_PEM = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def generate_token(user_id: int, extra_claims: Optional[dict] = None) -> str:
    payload = {
        "sub": str(user_id),
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, PRIVATE_KEY_PEM, algorithm="RS256")

def verify_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, PUBLIC_KEY_PEM, algorithms=["RS256"])
    except jwt.PyJWTError:
        return None