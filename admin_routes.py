from fastapi import APIRouter, Depends, HTTPException
from auth import verify_token
from database import db

router = APIRouter(tags=["Admin Only"])

@router.get("/stats")
async def get_stats(token_data: dict = Depends(verify_token)):
    return {
        "total_events": db.events.count_documents({}),
        "total_registrations": db.registrations.count_documents({}),
        "total_checkins": db.checkins.count_documents({}),
        "attendance_rate": f"{(db.checkins.count_documents({})/db.registrations.count_documents({})*100 if db.registrations.count_documents({}) > 0 else 0):.1f}%"
    }