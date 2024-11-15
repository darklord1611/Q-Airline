

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime

router = APIRouter(prefix="/aircrafts", tags=["aircrafts"])


@router.get("", description="Get all aircrafts")
async def get_aircrafts(
):
    aircrafts = supabase.table("aircrafts").select().execute().data
    return {"status" : "success", "data": aircrafts}



