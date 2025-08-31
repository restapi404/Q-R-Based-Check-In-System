from fastapi import APIRouter, Depends, HTTPException
import qrcode
import os
from email_service import send_qr_email
from database import db
from auth import check_step
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/qrcode")
async def generate_qr(
    event_id: str,
    token_data: dict = Depends(check_step("qr"))
):
    # Verify registration
    if not db.registrations.find_one({"email": token_data["email"], "event_id": event_id}):
        raise HTTPException(status_code=403, detail="Not registered for this event")
    
    # Generate QR code
    qr_data = f"{token_data['email']}|{event_id}"
    qr_path = f"qrcodes/{token_data['email']}_{event_id}.png"
    os.makedirs("qrcodes", exist_ok=True)
    qrcode.make(qr_data).save(qr_path)
    
    # Get event details
    event = db.events.find_one({"id": event_id}, {"_id": 0})
    
    # Send email
    send_qr_email(
        to_email=token_data["email"],
        event_name=event["title"],
        qr_path=qr_path
    )
    
    return {
        "message": "QR code generated and sent to your email",
        "event": event,
        "qr_image": FileResponse(qr_path)
    }