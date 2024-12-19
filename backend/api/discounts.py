

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateDiscountRequest

router = APIRouter(prefix="/discounts", tags=["discounts"])


@router.get("", description="Get all discounts")
async def get_discounts(
):
    discounts = supabase.table("discounts").select().eq("is_active", True).execute().data
    return {"status" : "success", "data": discounts}


@router.post("", description="Create new discount")
async def create_discount(req: CreateDiscountRequest):

    res = supabase.table("discounts").insert({
        "name": req.name,
        "discount_factor": req.discount_factor,
        "start_time": req.start_time,
        "end_time": req.end_time,
        "is_active": req.is_active,
        "image_url": req.image_url,
    }).execute().data[0]

    return {"status": "success", "data": res}