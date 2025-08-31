from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

security = HTTPBearer()

class TokenData(BaseModel):
    email: str
    current_step: str  # register → browse → qr
    exp: datetime

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def create_token(email: str, current_step: str) -> str:
    payload = {
        "email": email,
        "current_step": current_step,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY", "secret"), algorithm="HS256")

async def verify_token(token: str = Depends(security)) -> dict:
    try:
        payload = jwt.decode(token.credentials, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_step(required_step: str):
    async def dependency(token_data: dict = Depends(verify_token)):
        if token_data.get("current_step") != required_step:
            step_names = {
                "register": "registration",
                "browse": "event selection",
                "qr": "QR generation"
            }
            raise HTTPException(
                status_code=403,
                detail=f"Please complete {step_names.get(token_data.get('current_step'))} step first"
            )
        return token_data
    return dependency