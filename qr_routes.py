'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import qrcode
import io
from fastapi.responses import StreamingResponse
from database import db

# Initialize the API router for QR-code-related routes
router = APIRouter()

# Schema for check-in
class CheckIn(BaseModel):
    email: str

@router.get("/generate")
async def generate_qr(event_id: str):
    # Generate a QR code for the given event ID
    qr_data = f"event:{event_id}"
    qr = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

@router.post("/checkin")
async def check_in(data: CheckIn):
    # Verify if the user exists
    if not db.users.find_one({"email": data.email}):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Record the check-in
    db.checkins.insert_one({"email": data.email})
    return {"message": "Check-in successful"}'''

'''
from fastapi import APIRouter, Depends, HTTPException
import qrcode
import io
from auth import verify_token
from database import db

router = APIRouter()

@router.get("/generate")
async def generate_qr(event_id: str, token: str = Depends(verify_token)):
    user_email = token["email"]
    qr_data = f"{user_email}|{event_id}"
    
    # Simple QR generation
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@router.post("/checkin")
async def check_in(qr_data: str):
    try:
        email, event_id = qr_data.split("|")
        db.checkins.insert_one({"email": email, "event_id": event_id})
        return {"message": "Checked in!"}
    except:
        raise HTTPException(400, "Invalid QR code")
'''


from fastapi import APIRouter, Depends
from auth import check_step
from database import db
import qrcode
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/qrcode")
async def generate_qr(
    event_id: str,
    token: str = Depends(lambda: check_step(token, "qr"))
):
    email = check_step(token, "qr")["email"]
    
    # Verify registration
    if not db.registrations.find_one({"email": email, "event_id": event_id}):
        return {
            "message": "You haven't registered for this event yet.",
            "solution": "First register at POST /api/events/register"
        }
    
    # Generate QR code
    qr_data = f"{email}|{event_id}"
    os.makedirs("qrcodes", exist_ok=True)
    filepath = f"qrcodes/{email}_{event_id}.png"
    
    qr = qrcode.make(qr_data)
    qr.save(filepath)
    
    return {
        "message": "QR code generated successfully!",
        "qr_code": FileResponse(filepath),
        "instructions": "Show this QR code at the event entrance for check-in"
    }

@router.post("/checkin")
async def check_in(qr_data: str):
    try:
        email, event_id = qr_data.split("|")
    except:
        return {
            "message": "Invalid QR code format",
            "solution": "Scan a valid event QR code"
        }
    
    # Verify registration
    if not db.registrations.find_one({"email": email, "event_id": event_id}):
        return {
            "message": "Registration not found",
            "solution": "This user hasn't registered for the event"
        }
    
    # Mark check-in
    db.checkins.insert_one({
        "email": email,
        "event_id": event_id,
        "timestamp": datetime.utcnow()
    })
    
    return {
        "message": f"Check-in successful for {email}",
        "event": db.events.find_one({"id": event_id}, {"_id": 0})
    }