

from fastapi import APIRouter, Body
from supabase_client import supabase
from utils.request_models import CreateNotificationRequest
from utils.util import convert_timestamp

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
    notifications = supabase.table("notification_user").select("notification_id, is_read, notifications!notification_user_notification_id_fkey(title, description, type)").eq("user_id", user_id).execute().data

    return {"status": "success", "data": notifications}

@router.get("/{user_id}/latest")
async def get_latest_user_notification(user_id: str):
    # get the latest notification
    notification = supabase.table("notification_user").select("notification_id, is_read, notifications!notification_user_notification_id_fkey(title, description, type)").eq("user_id", user_id).order("notification_id", desc=True).limit(1).execute().data[0]

    return {"status": "success", "data": notification}