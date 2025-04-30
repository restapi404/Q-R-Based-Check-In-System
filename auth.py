'''import bcrypt

# Hash a plain-text password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

# Verify a plain-text password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))'''
'''
import bcrypt
import jwt
from datetime import datetime, timedelta

# Simple JWT setup
SECRET_KEY = "your-simple-secret-key"  # Just use a simple string
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_token(email: str) -> str:
    return jwt.encode({"email": email}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])'''

from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()

class TokenData(BaseModel):
    email: str
    current_step: str  # register → browse → qr

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_token(email: str, current_step: str) -> str:
    payload = {
        "email": email,
        "current_step": current_step,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return raw dict instead of TokenData
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please login again."
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please login."
        )

async def check_step(required_step: str = "browse"):
    async def dependency(token_data: dict = Depends(verify_token)):
        if token_data.get("current_step") != required_step:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Please complete your {token_data.get('current_step')} step first."
            )
        return token_data
    return dependency