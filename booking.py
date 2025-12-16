from front_end_functions import list_prices
from pydantic import BaseModel
from db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory
from user_input_functions import ask_for_age, ask_for_amount_of_travelers, ask_for_ski_category

class TravelerBooking(BaseModel):
    age_category: AgeCategory
    ski_category: SkiCategory
    price: int


class Booking(BaseModel):
    traveler_bookings: list[TravelerBooking]
    total_price: int


#TODO Could probably do a better fault handling using exceptions here and not None returns
#TODO Incorporate destination weather data into price calculation
def calculate_traveler_price(prices: list[PriceEntry], age_category_id: int, ski_category_id: int) -> int | None:
    for record in prices:
        if record.agecatid == age_category_id and record.skiid == ski_category_id:
            return record.price
    return None


#TODO Maybe use exceptions here and not prints?
#TODO Incorporate destination weather data into price calculation
def calculate_booking_price(
    traveler_bookings: list[TravelerBooking],
) -> int:
    total_price = 0
    for booking in traveler_bookings:
        if booking.price:
            total_price += booking.price
        else:
            print(f"No price found for this combination {booking.age_category.name} and {booking.ski_category.name}.")

    return total_price


#TODO Could probably do a better fault handling using exceptions here and not None returns
def create_booking(
    travelers: int,
    prices: list[PriceEntry],
    age_categories: dict[int, AgeCategory],
    ski_categories: dict[int, SkiCategory],
) -> Booking | None:
    traveler_bookings: list[TravelerBooking] = []
    for traveler in range(1, travelers+1):
        print(f"Traveler {traveler}/{travelers}:")

        age_category_id = ask_for_age(age_categories)
        if not age_category_id:
            return

        subset_age_categories = {k: age_categories[k] for k in age_categories if k == age_category_id}
        list_prices(prices, subset_age_categories, ski_categories)

        ski_category_id = ask_for_ski_category(ski_categories)
        if not ski_category_id:
            return

        traveler_bookings.append(
            TravelerBooking(
                age_category=age_categories[age_category_id],
                ski_category=ski_categories[ski_category_id],
                price=calculate_traveler_price(prices, age_category_id, ski_category_id),
            )
            )

    total_price = calculate_booking_price(traveler_bookings)
    return Booking(traveler_bookings=traveler_bookings, total_price=total_price)


#TODO Could probably do a better fault handling using exceptions here and not None returns
def start_booking() -> Booking | None:
    # Fetch latest data
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    age_categories = db_client.fetch_age_categories()
    ski_categories = db_client.fetch_ski_categories()
    db_client.close()

    list_prices(prices, age_categories, ski_categories)

    travelers = ask_for_amount_of_travelers()
    if not travelers:
        return None

    return create_booking(travelers, prices, age_categories, ski_categories)


def print_booking(booking: Booking) -> None:
    print(f"\nBooking for {len(booking.traveler_bookings)} traveler(s)")
    print("Prices:\n")
    for traveler_booking in booking.traveler_bookings:
        print(f"{traveler_booking.age_category.name} {traveler_booking.ski_category.name} {traveler_booking.price} SEK")
    print(f"\nTotal Price: {booking.total_price} SEK\n")
