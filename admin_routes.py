'''from fastapi import APIRouter, Depends, HTTPException
from auth import verify_token
from database import db

router = APIRouter()

@router.get("/stats/{event_id}")
async def get_event_stats(event_id: str, token: str = Depends(verify_token)):
    # Simple admin check (in real app, verify role from token)
    if not db.users.find_one({"email": token["email"], "role": "admin"}):
        raise HTTPException(403, "Admin access required")
    
    total = db.registrations.count_documents({"event_id": event_id})
    checked_in = db.registrations.count_documents({
        "event_id": event_id,
        "checked_in": True
    })
    
    return {
        "total_registrations": total,
        "checked_in": checked_in,
        "attendance_rate": f"{(checked_in/total)*100:.1f}%" if total > 0 else "0%"
    }'''

from fastapi import APIRouter, Depends
from auth import verify_token
from database import db

router = APIRouter(tags=["Admin Only"])

@router.get("/stats")
async def get_stats(token: str = Depends(verify_token)):
    return {
        "total_events": db.events.count_documents({}),
        "total_registrations": db.registrations.count_documents({}),
        "total_checkins": db.checkins.count_documents({})
    }