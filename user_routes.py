'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import db
from auth import hash_password, verify_password

# Initialize the API router for user-related routes
router = APIRouter()

# Schema for user registration
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str

# Schema for user login
class LoginUser(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(user: RegisterUser):
    try:
        # Check if the email is already registered
        if db.users.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password and save the user to the database
        hashed_password = hash_password(user.password)
        db.users.insert_one({"name": user.name, "email": user.email, "password": hashed_password})
        return {"message": "User registered successfully"}
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login")
async def login(user: LoginUser):
    try:
        # Find the user by email
        db_user = db.users.find_one({"email": user.email})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Return a success message
        return {"message": "Login successful"}
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred during login: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")'''

'''
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from database import db
from auth import hash_password
from typing import Optional

router = APIRouter()

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: RegisterUser):
    try:
        # Check if user exists
        if db.users.find_one({"email": user.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_pw = hash_password(user.password)
        
        # Insert new user
        result = db.users.insert_one({
            "name": user.name,
            "email": user.email,
            "password": hashed_pw,
            "role": "student",
            "created_at": datetime.utcnow()
        })
        
        # Return the inserted user ID
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id),
            "email": user.email
        }
        
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)  # Return actual error message
        )'''

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database import db
from auth import hash_password, verify_password, create_token

router = APIRouter()

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: RegisterUser):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered. Please login instead."
        )
    
    db.users.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": "student"
    })
    return {
        "message": "Registration successful! Now please login.",
        "next_step": "POST /api/login with your credentials"
    }

@router.post("/login")
async def login(user: LoginUser):
    db_user = db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password. Please try again."
        )
    
    return {
        "message": "Login successful! You can now browse events.",
        "token": create_token(db_user["email"], "browse"),
        "next_step": "GET /api/events to see available events"
    }