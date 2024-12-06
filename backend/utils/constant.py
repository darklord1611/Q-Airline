from enum import Enum

class TRIP_TYPE(str, Enum):
    one_way = "ONE_WAY"
    round_trip = "ROUND_TRIP"

class BOOKING_STATUS(str, Enum):
    pending = "PENDING"
    confirmed = "CONFIRMED"
    cancelled = "CANCELLED"

class GENDER(str, Enum):
    male = "MALE"
    female = "FEMALE"