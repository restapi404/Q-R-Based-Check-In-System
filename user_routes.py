from fastapi import APIRouter, HTTPException
import bcrypt
from database import db
from auth import hash_password, create_token

router = APIRouter()

@router.post("/register")
async def register(name: str, email: str, password: str):
    if db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db.users.insert_one({
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": "student"
    })
    return {"message": "Registration successful"}

@router.post("/login")
async def login(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Convert stored password from string to bytes
    hashed_password = user["password"].encode('utf-8')
    
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "token": create_token(email, "browse"),
        "message": "Login successful"
    }