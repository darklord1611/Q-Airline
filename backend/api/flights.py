

from fastapi import APIRouter, Body
from supabase_client import supabase

router = APIRouter(prefix="/flights")


@router.get("/search")
async def get_flights(req):
    arrival_airport_id = req.query_params.get("arrival_airport_id")
    departure_airport_id = req.query_params.get("departure_airport_id")
    departure_date = req.query_params.get("departure_date")
    route_id = supabase.table("routes").select("id").eq("arrival_airport_id", arrival_airport_id).eq("departure_airport_id", departure_airport_id).execute().data[0]["id"]
    flights = supabase.table("flights").select().eq("route_id", route_id).eq("departure", departure_date).execute().data
    return {"flights": "flights"}
