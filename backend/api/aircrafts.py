

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime

router = APIRouter(prefix="/aircrafts", tags=["aircrafts"])


@router.get("", description="Get all aircrafts")
async def get_aircrafts(
):
    aircrafts = supabase.table("aircrafts").select().execute().data
    return {"status" : "success", "data": aircrafts}

# TEMPORARY
@router.post("", description="Create a new aircraft")
async def create_aircraft(
    registration: str = Form(...),
    model: str = Form(...),
    make: str = Form(...),
    year: int = Form(...),
    capacity: int = Form(...),
    status: str = Form(...),
    created_at: str = Body(default=str(datetime.now())),
    updated_at: str = Body(default=str(datetime.now()))
):
    res = supabase.table("aircrafts").insert({
        "registration": registration,
        "model": model,
        "make": make,
        "year": year,
        "capacity": capacity,
        "status": status,
        "created_at": created_at,
        "updated_at": updated_at
    }).execute()

    return {"status": "success", "data": res.data[0]}

