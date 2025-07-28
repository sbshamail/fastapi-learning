from typing import Dict, Optional
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta
from practice.config import SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, password_hashed: str) -> bool:
    return pwd_context.verify(plain, password_hashed)


def create_access_token(data: dict,refresh: Optional[bool] = False, expires_delta: timedelta = None):
  
    expiration_time = (datetime.now(datetime.timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
                if not refresh
                        else None  # If refresh is True, no expiration
              
              )
  
    payload = {
        "user": data,
        "exp": expiration_time,
        "refresh": refresh,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> Optional[Dict]:
    try:
        token_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},  # Ensure expiration is verified
        )

        return token_data

    except JWTError as e:
        print(f"Token decoding failed: {e}")
        return None
