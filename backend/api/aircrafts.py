

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateAircraftRequest

router = APIRouter(prefix="/aircrafts", tags=["aircrafts"])


def calc_total_capacity(seat_configuration: dict):
    total_capacity = 0
    for key, value in seat_configuration.items():
        total_capacity += value["rows"] * value["cols"]

    return total_capacity

@router.get("", description="Get all aircrafts")
async def get_aircrafts(
):
    aircrafts = supabase.table("aircrafts").select("id", "model", "manufacturer").execute().data
    return {"status" : "success", "data": aircrafts}

# TEMPORARY
@router.post("", description="Create a new aircraft")
async def create_aircraft(req: CreateAircraftRequest):

    req.total_capacity = calc_total_capacity(req.seat_configuration)

    res = supabase.table("aircrafts").insert({
        "model": req.model,
        "manufacturer": req.manufacturer,
        "total_capacity": req.total_capacity,
        "seat_configuration": req.seat_configuration
    }).execute().data[0]

    print(res)

    
    # create seats according to the seat configuration

    create_seats_res = supabase.rpc("create_seats_for_aircraft", params={"_aircraft_id": res["id"], "seat_config": req.seat_configuration}).execute().data
    print(create_seats_res)
    return {"status": "success", "data": res["id"]}

