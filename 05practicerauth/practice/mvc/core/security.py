from typing import Dict, Optional
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select
from practice.mvc.models.userModel import User
from practice.config import SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## get user
def exist_user(db: Session, email: str):
    user = db.exec(select(User).where(User.email == email)).first()
    return user


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, password_hashed: str) -> bool:
    return pwd_context.verify(plain, password_hashed)


def create_access_token(
        user_data: dict,
        refresh: Optional[bool] = False, 
        expires: timedelta = None
    ):

    if refresh:
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    else:
        expire = datetime.now(timezone.utc) + (expires or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
          
    payload = {
        "user": user_data,
        "exp": expire,
        "refresh": refresh,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> Optional[Dict]:
    try:
        decode = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},  # Ensure expiration is verified
        )

        return decode

    except JWTError as e:
        print(f"Token decoding failed: {e}")
        return None
