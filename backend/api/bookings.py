

from fastapi import APIRouter, Body, Form
from typing import Optional
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateBookingRequest

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", description="Get all bookings")
async def get_bookings(flight_id: Optional[str] = None, user_id: Optional[str] = None):
    if flight_id:
        bookings = supabase.from_("booking_flight").select("bookings!booking_flight_booking_id_fkey(*)").eq("flight_id", flight_id).execute().data
    elif user_id:
        bookings = supabase.table("bookings").select().eq("user_id", user_id).execute().data
    else:
        bookings = supabase.table("bookings").select().execute().data
    return {"status" : "success", "data": bookings}

@router.post("", description="Create a new booking")
async def create_booking(req: CreateBookingRequest):

    res = supabase.table("bookings").insert({
        "user_id": req.user_id,
        "booking_status": req.booking_status,
        "total_amount": req.total_amount,
        "number_of_passengers": len(req.passengers),
        "class_name": req.class_name,
        "trip_type": req.trip_type
    }).execute()

    booking_id = res.data[0]['id']
    # associate booking with flight
    res = supabase.table("booking_flight").insert({
        "booking_id": booking_id,
        "flight_id": req.flight_id,
        "leg_number": 1 # ONE_WAY TRIP
    }).execute()

    booking_flight_id = res.data[0]['id']
    
    passenger_records = []
    # create passenger records
    for i in range(len(req.passengers)):
        passenger_records.append({
            "first_name": req.passengers[i].first_name,
            "last_name": req.passengers[i].last_name,
            "email": req.passengers[i].email,
            "gender": req.passengers[i].gender,
            "birthday": req.passengers[i].birthday,
            "phone": req.passengers[i].phone,
        })
    
    passenger_res = supabase.table("passengers").insert(passenger_records).execute()

    # associate seats with passengers
    for i in range(len(passenger_res.data)):
        passenger_id = passenger_res.data[i]['id']
        seat_id = req.passengers[i].seat_id
        relation_res = supabase.table("booking_passenger_seat").insert({
            "booking_flight_id": booking_flight_id,
            "passenger_id": passenger_id,
            "seat_id": seat_id
        }).execute()

        # update seat availability
        _ = supabase.table("flight_seat_availability").update({"is_available": False}).eq("flight_id", req.flight_id).eq("seat_id", seat_id).execute()

    
    return {"status" : "success", "data": res.data}


@router.delete("/{booking_id}", description="Cancel a booking")
async def cancel_booking(booking_id: str):
    res = supabase.table("bookings").update({"booking_status": "CANCELLED"}).eq("id", booking_id).execute()
    return {"status" : "success", "data": res.data[0]}
