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


class CreateFlightRequest(BaseModel):
    departure_airport_id: int
    arrival_airport_id: int
    departure_time: str
    arrival_time: str
    aircraft_id: int
    flight_status: str = "SCHEDULED"
    is_active: bool = True
    class_pricing: dict = TEMPLATE_PRICING

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
    total_amount: float = 0
    class_name: str
    trip_type: TRIP_TYPE = TRIP_TYPE.one_way
    passengers: list
