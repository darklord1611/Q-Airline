

from fastapi import APIRouter, Body, UploadFile, File
from supabase_client import supabase
from utils.request_models import CreateNewsRequest
router = APIRouter(prefix="/news", tags=["news"])

@router.get("")
async def get_news():
    news = supabase.table("news").select().eq("visibility", "PUBLIC").eq("category", "Promotion").order("created_at", desc=True).execute().data
    return {"status": "success", "data": news}



@router.get("/destinations")
async def get_destination_news():
    news = supabase.table("news").select().eq("visibility", "PUBLIC").eq("category", "Destination").execute().data
    return {"status": "success", "data": news}



@router.get("/promotions")
async def get_promotion_news():
    news = supabase.table("news").select().eq("visibility", "PUBLIC").eq("category", "Promotion").order("created_at", desc=True).execute().data
    return {"status": "success", "data": news}


@router.post("")
async def create_news(req: CreateNewsRequest):

    res = supabase.table("news").insert({
        "author_id": req.author_id,
        "title": req.title,
        "body": req.body,
        "category": req.category,
        "visibility": req.visibility,
        "image_url": req.image_url,
        "external_article_link": req.external_article_link
    }).execute().data[0]

    return {"status": "success", "data": res}


@router.delete("/{news_id}")
async def delete_news(news_id: int):
    res = supabase.table("news").delete().eq("id", news_id).execute().data[0]
    return {"status": "success", "data": res}

