

from fastapi import APIRouter, Body
from supabase_client import supabase

router = APIRouter(prefix="/airports", tags=["airports"])


@router.get("")
async def get_airports():
    airports = supabase.table("airports").select("id", "iata_code", "city").execute().data
    return {"status": "success", "data": airports}

@router.get("/{departure_airport_id}/get_arrival_airports")
async def get_arrival_airports(departure_airport_id: int):
    routes = supabase.table("routes").select("arrival_airport_id").eq("departure_airport_id", departure_airport_id).execute().data
    arrival_airport_ids = [route["arrival_airport_id"] for route in routes]
    arrival_airports = supabase.table("airports").select("id", "iata_code", "city").in_("id", arrival_airport_ids).execute().data
    return {"status": "success", "data": arrival_airports}

@router.get("/{arrival_airport_id}/get_departure_airports")
async def get_departure_airports(arrival_airport_id: int):
    routes = supabase.table("routes").select("departure_airport_id").eq("arrival_airport_id", arrival_airport_id).execute().data
    departure_airport_ids = [route["departure_airport_id"] for route in routes]
    departure_airports = supabase.table("airports").select("id", "iata_code", "city").in_("id", departure_airport_ids).execute().data
    return {"status": "success", "data": departure_airports}

# @router.get("/get_departure_airports")
# async def get_departure_airports():
#     routes = supabase.rpc("get_distinct_departure_airport_ids").execute().data
#     departure_airport_ids = [route["departure_airport_id"] for route in routes]
#     departure_airports = supabase.table("airports").select("id", "iata_code", "city").in_("id", departure_airport_ids).execute().data
#     return {"status": "success", "data": departure_airports}





