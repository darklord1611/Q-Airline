

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateAircraftRequest

router = APIRouter(prefix="/discounts", tags=["discounts"])


@router.get("", description="Get all discounts")
async def get_discounts(
):
    discounts = supabase.table("discounts").select().eq("is_active", True).execute().data
    return {"status" : "success", "data": discounts}


