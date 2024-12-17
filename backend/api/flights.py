

from fastapi import APIRouter, Body, Form
from supabase_client import supabase
from datetime import datetime
from utils.request_models import CreateFlightRequest, GetFlightRequest, UpdateFlightRequest
from utils.util import convert_timestamp_to_time, time_difference, convert_timestamp, convert_timestamp_to_date
router = APIRouter(prefix="/flights", tags=["flights"])



@router.get("", description="Get all flights")
async def get_all_flights():

    flights = supabase.from_("flight_details").select().execute().data

    # flights = supabase.table("flights").select().execute().data
    # for flight in flights:
    #     flight["class_pricing"] = supabase.table("flight_class_pricing").select("class_name", "base_price", "tax_percentage", "discount_percentage").eq("flight_id", flight["id"]).execute().data

    #     flight["aircraft_info"] = supabase.table("aircrafts").select("model", "manufacturer").eq("id", flight["aircraft_id"]).execute().data
    
    return {"status" : "success", "data": flights}

@router.get("/search", description="Get all flights that match the search criteria")
async def get_flights(departure_airport_id: int, arrival_airport_id: int, departure_date: str):
    try:
        print(departure_date)
        # Parse the input date to get the date part only
        date_obj = datetime.fromisoformat(departure_date.rstrip("Z") + "+00:00")
        date_str = date_obj.strftime('%Y-%m-%d')  # Format to 'YYYY-MM-DD'
        print(date_str)
        route_id = supabase.table("routes").select("id").eq("arrival_airport_id", arrival_airport_id).eq("departure_airport_id", departure_airport_id).execute().data[0]["id"]

        flights = supabase.table("flights").select().eq("route_id", route_id).eq("is_active", True).gte("departure_time", f"{date_str}T00:00:00Z").lt("departure_time", f"{date_str}T23:59:59Z").execute().data

        for flight in flights:
            flight["class_pricing"] = supabase.table("flight_class_pricing").select("class_name", "base_price", "tax_percentage", "discount_percentage").eq("flight_id", flight["id"]).execute().data
            flight["aircraft_info"] = supabase.table("aircrafts").select("model", "manufacturer").eq("id", flight["aircraft_id"]).execute().data        
            flight["checkin"] = convert_timestamp_to_date(flight["departure_time"])
            flight["checkout"] = convert_timestamp_to_date(flight["arrival_time"])
            flight["departure_time"] = convert_timestamp_to_time(flight["departure_time"])
            flight["arrival_time"] = convert_timestamp_to_time(flight["arrival_time"])
            flight["duration"] = time_difference(flight["departure_time"], flight["arrival_time"])
            
        return {"status" : "success", "data": flights}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/{flight_id}/seats", description="Get available seats of a flight")
async def get_available_seats(
    flight_id : int
):
    available_seats = supabase.table("flight_seat_availability").select("seat_id, is_available, seats!flight_seat_availability_seat_id_fkey(class_name, seat_number)").eq("flight_id", flight_id).order("id", desc=False).execute().data
    # only fetch the first 10 rows of the available seats
    return {"status": "success", "data": available_seats[:54]}

@router.post("")
async def create_flight(req: CreateFlightRequest):

    route_id = supabase.table("routes").select("id").eq("arrival_airport_id", req.arrival_airport_id).eq("departure_airport_id", req.departure_airport_id).execute().data[0]["id"]
    res = supabase.table("flights").insert({
        "route_id": route_id,
        "departure_time": req.departure_time,
        "arrival_time": req.arrival_time,
        "aircraft_id": req.aircraft_id,
        "flight_number": "AB123",
        "flight_status": req.flight_status,
        "is_active": req.is_active
    }).execute()

    flight_id = res.data[0]["id"]

    for class_name, pricing in req.class_pricing.items():
        pricing_res = supabase.table("flight_class_pricing").insert({
            "flight_id": flight_id,
            "class_name": class_name,
            "base_price": pricing["base_price"],
            "tax_percentage": pricing["tax_percentage"]
        }).execute()
    
    seat_associate_response = supabase.rpc("associate_seats_with_flight", {"flight_id": flight_id, "_aircraft_id" : req.aircraft_id}).execute()

    return {"status": "success", "data": res.data[0]}

@router.put("/{flight_id}")
async def update_flight(req: UpdateFlightRequest, flight_id: int):
    # deactivate the old flight
    response = supabase.table("flights").select().eq("id", flight_id).execute().data[0]

    # save flight history
    response["flight_id"] = response.pop("id")
    insert_history_response = supabase.table("flight_audit").insert(response).execute()
    

    update_response = supabase.table("flights").update({
        "departure_time": req.departure_time,
        "arrival_time": req.arrival_time,
        "flight_status": req.flight_status,
    }).eq("id", flight_id).execute()

    # update pricing if there are changes to the pricing

    for pricing in req.class_pricing:
        pricing_res = supabase.table("flight_class_pricing").update({
            "base_price": pricing["base_price"],
            "tax_percentage": pricing["tax_percentage"]
        }).eq("flight_id", flight_id).eq("class_name", pricing["class_name"]).execute()

    
    # send out notifications about changes to customers

    flight_users = supabase.table("booking_flight").select("booking_id, bookings!booking_flight_booking_id_fkey(user_id)").eq("flight_id", flight_id).execute().data

    res = await notify_users(flight_users, response, req)

    return {"status": "success", "data": flight_users}

@router.delete("/{flight_id}")
async def delete_flight(flight_id: int):
    res = supabase.table("flights").delete().eq("id", flight_id).execute()
    return {"status": "success", "data": res.data[0]}

@router.get("/{flight_id}/history", description="Get history of a flight")
async def get_flight_history(flight_id: int):
    flight_history = supabase.table("flight_audit").select().eq("flight_id", flight_id).execute().data
    return {"status": "success", "data": flight_history}



@router.get("/{flight_id}/analytics", description="Get analytics of a flight")
async def get_flight_statistics(flight_id: int):
    # seat + class utilization
    # revenue generated
    # customer demographics
    flight_info = supabase.from_("flight_details").select().eq("flight_id", flight_id).execute().data[0]
    
    flight_info["service_statistics"] = supabase.table("flight_revenues").select().eq("flight_id", flight_id).execute().data
    return {"status": "success", "data": flight_info}


@router.get("/analytics", description="Get analytics of all flights")
async def get_all_flights_statistics(flight_id: int):
    
    pass



async def notify_users(flight_users, old_flight_info, new_flight_info):
    # notify users about the changes to flight schedule

    old_depart_time = convert_timestamp(old_flight_info["departure_time"])
    new_depart_time = convert_timestamp(new_flight_info.departure_time)

    message = f"Flight schedule for flight {old_flight_info['flight_number']} has been changed from {old_depart_time} to {new_depart_time}. Please check your booking for more details."

    notify_res = supabase.table("notifications").insert({
        "title": f"Flight Schedule Changed",
        "description": message,
        "notification_type": "SCHEDULE_CHANGE"
    }).execute().data[0]

    res = supabase.rpc("associate_users_with_notification", params={"notification_id": notify_res["id"], "user_ids": [user["bookings"]["user_id"] for user in flight_users]}).execute()
    print(res)
    return res



@router.get("/{flight_id}/class_pricings", description="Get available class_pricings of a flight")
async def get_class_pricings(
    flight_id : int
):
    class_pricings = supabase.table("flight_class_pricing").select().eq("flight_id", flight_id).execute().data
    return {"status": "success", "data": class_pricings}