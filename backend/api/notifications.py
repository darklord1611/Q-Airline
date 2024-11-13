

from fastapi import APIRouter, Body
from supabase_client import supabase

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def get_notifications():
    notifications = supabase.table("notifications").select().execute().data
    return {"status": "success", "data": notifications}


@router.post("")
async def create_notification(req):
    res = supabase.table("notifications").insert({
        "user_id": req.user_id,
        "title": req.title,
        "message": req.message,
        "is_read": req.is_read
    }).execute()

    return {"status": "success", "data": res.data[0]}

@router.get("/{user_id}")
async def get_user_notifications(user_id: str):
    notifications = supabase.table("notifications").select().eq("user_id", user_id).execute().data
    return {"status": "success", "data": notifications}