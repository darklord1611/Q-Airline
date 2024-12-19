from pydantic import BaseModel
from typing import Optional, Dict, List
from .constant import TRIP_TYPE, BOOKING_STATUS, GENDER
from .util import generate_random_phone_number

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

TEMPLATE_PRICING_2 = [
    {
        "class_name": "ECONOMY",
        "base_price": 50,
        "tax_percentage": 10
    },
    {
        "class_name": "BUSINESS",
        "base_price": 250,
        "tax_percentage": 10
    }
]


################## AUTH ##################
class RegisterRequest(BaseModel):
    password: str
    email: str
    first_name: str
    last_name: str
    username: Optional[str] = None
    phone : str = generate_random_phone_number("VN")
    role: str = "user"


class LoginRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

class LogoutRequest(BaseModel):
    token: str

################## FLIGHTS ##################
class CreateFlightRequest(BaseModel):
    flight_number: str
    departure_airport_id: int
    arrival_airport_id: int
    departure_time: str
    arrival_time: str
    aircraft_id: int
    flight_status: str = "SCHEDULED"
    is_active: bool = True
    class_pricing: list = TEMPLATE_PRICING_2
    

class UpdateFlightRequest(BaseModel):
    flight_id: int
    departure_time: str
    arrival_time: str
    flight_status: str = "SCHEDULED"
    class_pricing: list

class GetFlightRequest(BaseModel):
    arrival_airport_id: int
    departure_airport_id: int
    departure_date: str


################## AIRCRAFTS ##################
class SeatLayout(BaseModel):
    business_rows: int
    economy_rows: int
    business_seats_per_row: int
    economy_seats_per_row: int

class CreateAircraftRequest(BaseModel):
    model: str
    manufacturer: str
    total_capacity: int = 0
    seat_configuration: dict


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
    place: str

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


################## NEWS ##################
class CreateNewsRequest(BaseModel):
    author_id: str
    title: str
    body: str
    category: str = "Promotion"
    visibility: str = "PUBLIC"
    image_url: str = ""
    external_article_link: str = ""

################## DISCOUNTS ##################

class CreateDiscountRequest(BaseModel):
    name: str
    description: str
    discount_factor: float
    image_url: str = ""
    start_time: str
    end_time: str
    is_active: bool = True