

from fastapi import APIRouter, Body
from supabase_client import supabase
from utils.request_models import CreateNotificationRequest

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def get_notifications():
    notifications = supabase.table("notifications").select().execute().data
    return {"status": "success", "data": notifications}


@router.post("")
async def create_notification(req: CreateNotificationRequest):
    res = supabase.table("notifications").insert({
        "title": req.title,
        "description": req.description,
        "type": req.type
    }).execute()

    return {"status": "success", "data": res.data[0]}

@router.get("/{user_id}")
async def get_user_notifications(user_id: str):
    notifications = supabase.table("notifications").select().eq("user_id", user_id).execute().data
    return {"status": "success", "data": notifications}