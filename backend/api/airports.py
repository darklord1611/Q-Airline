

from fastapi import APIRouter, Body
from supabase_client import supabase

router = APIRouter(prefix="/airports")


@router.get("/all")
async def get_airports():
    airports = supabase.table("airports").select().execute().data
    return {"status": "success", "data": airports}



