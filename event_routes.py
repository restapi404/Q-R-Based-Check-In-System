from fastapi import APIRouter, Depends, HTTPException
from database import db
from auth import check_step
from datetime import datetime

router = APIRouter()

@router.get("/events")
async def list_events(token_data: dict = Depends(check_step("browse"))):
    try:
        # Explicitly include the 'id' field in the projection
        events = list(db.events.find({}, {"_id": 0, "id": 1, "title": 1, "date": 1, "description": 1, "location": 1}))
        
        if not events:
            return {
                "message": "No events available",
                "events": []
            }
            
        return {
            "message": "Events retrieved successfully",
            "events": events
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching events: {str(e)}"
        )

@router.post("/events/register")
async def register_for_event(
    event_id: str, 
    token_data: dict = Depends(check_step("browse"))
):
    try:
        event = db.events.find_one({"id": event_id}, {"_id": 0})
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if db.registrations.find_one({"email": token_data["email"], "event_id": event_id}):
            return {"message": "Already registered for this event"}
        
        db.registrations.insert_one({
            "email": token_data["email"],
            "event_id": event_id,
            "registered_at": datetime.utcnow(),
            "checked_in": False
        })
        
        return {
            "token": create_token(token_data["email"], "qr"),
            "message": "Registered successfully",
            "event": event
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )