

from fastapi import APIRouter, Body
from supabase_client import supabase

router = APIRouter(prefix="/news", tags=["news"])


@router.get("")
async def get_news():
    news = supabase.table("news").select().execute().data
    return {"status": "success", "data": news}


@router.post("")
async def create_news(req):
    res = supabase.table("news").insert({
        "user_id": req.user_id,
        "title": req.title,
        "message": req.message,
        "is_read": req.is_read
    }).execute()

    return {"status": "success", "data": res.data[0]}
