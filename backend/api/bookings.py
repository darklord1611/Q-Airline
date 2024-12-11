

from fastapi import APIRouter, Body, Form
from typing import Optional
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateBookingRequest
from utils.util import convert_timestamp_to_time, time_difference, convert_timestamp_to_date
router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", description="Get all bookings of a specific condition")
async def get_bookings(flight_id: Optional[str] = None, user_id: Optional[str] = None):
    if flight_id:
        bookings = supabase.from_("booking_flight").select("bookings!booking_flight_booking_id_fkey(*)").eq("flight_id", flight_id).execute().data
    elif user_id:
        bookings = supabase.table("bookings").select().eq("user_id", user_id).execute().data
        for booking in bookings:
            # get flight ids according to the booking
            flights = supabase.from_("booking_flight").select("flight_id", "id").eq("booking_id", booking["id"]).execute().data
            booking["flights"] = []
            total_price = 0
            print(flights)
            for flight in flights:
                # get flight details
                temp_flight_info = supabase.from_("flight_details").select().eq("flight_id", flight["flight_id"]).execute().data[0]
                temp_flight_info["checkin"] = convert_timestamp_to_date(temp_flight_info["departure_time"])
                temp_flight_info["checkout"] = convert_timestamp_to_date(temp_flight_info["arrival_time"])
                temp_flight_info["departure_time"] = convert_timestamp_to_time(temp_flight_info["departure_time"])
                temp_flight_info["arrival_time"] = convert_timestamp_to_time(temp_flight_info["arrival_time"])
                temp_flight_info["duration"] = time_difference(temp_flight_info["departure_time"], temp_flight_info["arrival_time"])
                
                # get external services
                if flight["id"]:
                    temp_flight_info["services"] = supabase.from_("booking_flight_service").select("total_price", "quantity", "services!booking_flight_service_service_id_fkey(id, name, price, type)").eq("booking_flight_id", flight["id"]).execute().data
                    total_price += sum([service["total_price"] for service in temp_flight_info["services"]])
                booking["flights"].append(temp_flight_info)
            booking["total_price"] = total_price + booking["total_amount"] # price of external services + ticket price
    else:
        bookings = supabase.table("bookings").select().execute().data
    return {"status" : "success", "data": bookings}

@router.post("", description="Create a new booking")
async def create_booking(req: CreateBookingRequest):

    ticket_price = supabase.table("flight_class_pricing").select("base_price").eq("flight_id", req.flight_id).eq("class_name", req.class_name).execute().data[0]['base_price']
    # total amount here is the ticket price alone
    total_amount = ticket_price * len(req.passengers)

    res = supabase.table("bookings").insert({
        "user_id": req.user_id,
        "booking_status": req.booking_status,
        "total_amount": total_amount,
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

    # associate services with booking
    for service in req.services:
        service_price = supabase.table("services").select("price").eq("id", service.service_id).execute().data[0]['price']
        _ = supabase.table("booking_flight_service").insert({
            "booking_flight_id": booking_flight_id,
            "service_id": service.service_id,
            "quantity": service.quantity,
            "total_price": service_price * service.quantity
        }).execute()
    
    return {"status" : "success", "data": res.data}


@router.patch("/{booking_id}", description="Cancel a booking")
async def cancel_booking(booking_id: str):
    res = supabase.table("bookings").update({"booking_status": "CANCELLED"}).eq("id", booking_id).execute()
    print(res)
    return {"status" : "success", "data": res.data[0]}
