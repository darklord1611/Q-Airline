

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateAircraftRequest

router = APIRouter(prefix="/aircrafts", tags=["aircrafts"])


@router.get("", description="Get all aircrafts")
async def get_aircrafts(
):
    aircrafts = supabase.table("aircrafts").select().execute().data
    return {"status" : "success", "data": aircrafts}

# TEMPORARY
@router.post("", description="Create a new aircraft")
async def create_aircraft(req: CreateAircraftRequest):
    res = supabase.table("aircrafts").insert({
        "model": req.model,
        "manufacturer": req.manufacturer,
        "total_capacity": req.total_capacity,
        "seat_configuration": req.seat_configuration
    }).execute()

    return {"status": "success", "data": res.data[0]}

