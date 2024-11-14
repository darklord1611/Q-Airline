from pydantic import BaseModel
from typing import Optional, Dict, List
from .constant import TRIP_TYPE, BOOKING_STATUS, GENDER


TEMPLATE_PRICING = {
    "ECONOMY": {
        "base_price": 50,
        "tax_percentage": 10
    },
    "BUSINESS": {
        "base_price": 250,
        "tax_percentage": 10
    }
}


################## AUTH ##################
class SignupRequest(BaseModel):
    password: str
    email: str
    first_name: str
    last_name: str
    username: Optional[str] = None
    phone : Optional[str] = None
    role: str = "user"


class LoginRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

class LogoutRequest(BaseModel):
    token: str

################## FLIGHTS ##################
class CreateFlightRequest(BaseModel):
    departure_airport_id: int
    arrival_airport_id: int
    departure_time: str
    arrival_time: str
    aircraft_id: int
    flight_status: str = "SCHEDULED"
    is_active: bool = True
    class_pricing: dict = TEMPLATE_PRICING


class UpdateFlightRequest(BaseModel):
    departure_time: str
    arrival_time: str
    aircraft_id: int
    flight_status: str = "SCHEDULED"

class GetFlightRequest(BaseModel):
    arrival_airport_id: int
    departure_airport_id: int
    departure_date: str


################## AIRCRAFTS ##################
class SeatLayout(BaseModel):
    class_name: str
    rows: int
    columns: int
    seat_number: List[str] = ["A", "B", "C", "D", "E", "F"]

class CreateAircraftRequest(BaseModel):
    model: str
    manufacturer: str
    total_capacity: int
    seat_configuration: List[SeatLayout]


################## BOOKINGS ##################
class InFlightService(BaseModel):
    service_id: int
    quantity: int

class Passenger(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: GENDER = GENDER.male
    phone: str
    birthday: str
    seat_id: int

class CreateBookingRequest(BaseModel):
    user_id: str
    flight_id: int
    booking_status: BOOKING_STATUS = BOOKING_STATUS.pending
    class_name: str
    trip_type: TRIP_TYPE = TRIP_TYPE.one_way
    passengers: List[Passenger]
    services: List[InFlightService]


################## NOTIFICATIONS ##################
class CreateNotificationRequest(BaseModel):
    title: str
    description: str
    type: str = "info"