'''from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import db
from auth import create_jwt_token
import qrcode

router = APIRouter()

class Event(BaseModel):
    title: str
    description: str
    location: str
    date: str
    time: str

class RegisterEvent(BaseModel):
    event_id: str

# Create a new event (Admin-only)
@router.post("/events/create")
async def create_event(event: Event):
    db.events.insert_one(event.dict())
    return {"message": "Event created successfully"}

# Register for an event
@router.post("/events/register")
async def register_for_event(registration: RegisterEvent, user=Depends()):
    event = db.events.find_one({"_id": registration.event_id})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    qr_data = f"{user['email']}|{registration.event_id}"
    qr = qrcode.make(qr_data)
    qr.save(f"{user['email']}_qr.png")
    db.registrations.insert_one({"user_id": user["_id"], "event_id": registration.event_id, "checked_in": False})
    return {"message": "Registered successfully. QR code generated"}'''
'''
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import db
from auth import verify_token
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter()

class Event(BaseModel):
    title: str
    description: str
    location: str
    date: str
    time: str

class RegisterEvent(BaseModel):
    event_id: str

# Create event (protected - needs admin token)
@router.post("/create")
async def create_event(event: Event, token: str = Depends(verify_token)):
    # In a real app, you would check if user is admin here
    db.events.insert_one(event.dict())
    return {"message": "Event created successfully"}

# List all events (public)
@router.get("/list")
async def list_events():
    events = list(db.events.find({}, {"_id": 0}))
    return {"events": events}

# Register for event (protected - needs user token)
@router.post("/register")
async def register_for_event(
    registration: RegisterEvent, 
    token: str = Depends(verify_token)
):
    user_email = token["email"]  # From your verify_token
    event = db.events.find_one({"id": registration.event_id})
    
    if not event:
        raise HTTPException(404, "Event not found")
    
    # Generate QR code
    qr_data = f"{user_email}|{registration.event_id}"
    qr_img = qrcode.make(qr_data)
    
    # Save registration
    db.registrations.insert_one({
        "email": user_email,
        "event_id": registration.event_id,
        "checked_in": False,
        "qr_data": qr_data
    })
    
    event = db.events.find_one({"id": registration.event_id})
    send_qr_email(user_email, event["title"])

    # Return QR code image
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# Check in with QR code (public)
@router.post("/checkin")
async def check_in(qr_data: str):
    registration = db.registrations.find_one({"qr_data": qr_data})
    
    if not registration:
        raise HTTPException(400, "Invalid QR code")
    
    if registration["checked_in"]:
        return {"message": "Already checked in"}
    
    db.registrations.update_one(
        {"_id": registration["_id"]},
        {"$set": {"checked_in": True}}
    )
    return {"message": "Checked in successfully"}'''


from fastapi import APIRouter, Depends, HTTPException, status
from auth import check_step, create_token, TokenData
from database import db
from datetime import datetime

router = APIRouter()

@router.get("/events")

async def list_events(token_data: TokenData = Depends(lambda: check_step("browse"))):
    try:
        # Get events from database
        events = list(db.events.find({}, {"_id": 0}))
        
        if not events:
            return {
                "message": "No events available yet",
                "solution": "Check back later or contact organizers"
            }
            
        return {
            "message": "Available events:",
            "events": events,
            "next_step": "POST /api/events/register with chosen event_id"
        }

    except HTTPException:
        # Re-raise auth/validation errors
        raise
        
    except Exception as e:
        # Handle database/other errors
        raise HTTPException(
            status_code=500,
            detail="Service temporarily unavailable. Please try again later."
        )

@router.post("/events/register")
async def register_for_event(
    event_id: str,
    token: str = Depends(check_step)
):
    """Register for an event"""
    payload = check_step(token, "browse")
    email = payload["email"]
    
    if not db.events.find_one({"id": event_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} not found"
        )
    
    if db.registrations.find_one({"email": email, "event_id": event_id}):
        return {
            "message": "Already registered",
            "next_step": "GET /api/qrcode?event_id=" + event_id
        }
    
    db.registrations.insert_one({
        "email": email,
        "event_id": event_id,
        "checked_in": False,
        "registered_at": datetime.utcnow()
    })
    
    return {
        "message": "Registration successful!",
        "token": create_token(email, "qr"),
        "next_step": f"GET /api/qrcode?event_id={event_id}"
    }