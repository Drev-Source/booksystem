from pydantic import BaseModel
from db_client import AgeCategory, SkiCategory

class TravelerBooking(BaseModel):
    age_category: AgeCategory
    ski_category: SkiCategory
    price: int


class Booking(BaseModel):
    traveler_bookings: list[TravelerBooking]
    total_price: int