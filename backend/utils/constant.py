from enum import Enum

class TRIP_TYPE(Enum):
    one_way = "ONE_WAY"
    round_trip = "ROUND_TRIP"

class BOOKING_STATUS(Enum):
    pending = "PENDING"
    confirmed = "CONFIRMED"
    cancelled = "CANCELLED"

class GENDER(Enum):
    male = "MALE"
    female = "FEMALE"