from clients.db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory
from clients.yr_client import YRClient
from front_end import list_prices, print_age_categories, print_divider, print_ski_categories
from pydantic import BaseModel
from utility.economy import get_price_reduction
from utility.exceptions import AbortBookingException, AbortException
from user_input import ask_for_age, ask_for_amount_of_travelers, ask_for_ski_category



class TravelerBooking(BaseModel):
    age_category: AgeCategory
    ski_category: SkiCategory
    price: int
    price_reduced: int


class Booking(BaseModel):
    traveler_bookings: list[TravelerBooking]
    total_price: int


def calculate_traveler_price(
    prices: list[PriceEntry],
    age_category_id: int,
    ski_category_id: int,
    age_categories: dict[int, AgeCategory],
) -> tuple[int, bool]:
    yr_client = YRClient()
    current_weather = yr_client.get_current_weather()

    if current_weather:
        reduction = 1

    for record in prices:
        if record.agecatid == age_category_id and record.skiid == ski_category_id:
            if current_weather:
                reduction = get_price_reduction(age_category_id,
                                                age_categories,
                                                current_weather.data.air_temperature
                                                )
            else:
                reduction = 1

            price = round(record.price * reduction)
            price_reduced = record.price - price
            return price, price_reduced

    raise ValueError(
        f"Couldn't find prices for age category with id {age_category_id} " \
        f"and ski category with id {ski_category_id}"
    )


def calculate_booking_price(
    traveler_bookings: list[TravelerBooking],
) -> int:
    total_price = 0
    for booking in traveler_bookings:
        if booking.price:
            total_price += booking.price

    return total_price


def create_booking(
    travelers: int,
    prices: list[PriceEntry],
    age_categories: dict[int, AgeCategory],
    ski_categories: dict[int, SkiCategory],
) -> Booking | None:
    traveler_bookings: list[TravelerBooking] = []
    for traveler in range(1, travelers+1):
        print_divider()
        print(f"Traveler {traveler}/{travelers}:")
        print_age_categories(age_categories)
        age_category_id = ask_for_age(age_categories)

        #List comprehension, create a subset of age_categories filtered on age_category_id
        subset_age_categories = {k: age_categories[k] for k in age_categories if k == age_category_id}
        list_prices(prices, subset_age_categories, ski_categories)

        print_ski_categories(ski_categories)
        ski_category_id = ask_for_ski_category(ski_categories)

        try:
            price, price_reduced = calculate_traveler_price(prices, age_category_id, ski_category_id, age_categories)
        except ValueError as e:
            print(repr(e))
            print("Using default price 0")
            price = 0
            price_reduced = 0

        traveler_bookings.append(
            TravelerBooking(
                age_category=age_categories[age_category_id],
                ski_category=ski_categories[ski_category_id],
                price=price,
                price_reduced=price_reduced,
            )
        )

    total_price = calculate_booking_price(traveler_bookings)
    return Booking(traveler_bookings=traveler_bookings, total_price=total_price)


def start_booking() -> Booking:
    # Fetch latest data
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    age_categories = db_client.fetch_age_categories()
    ski_categories = db_client.fetch_ski_categories()
    db_client.close()

    try:
        print_divider()
        travelers = ask_for_amount_of_travelers()
        booking = create_booking(travelers, prices, age_categories, ski_categories)
    except AbortException as e:
        raise AbortBookingException("Cancel booking")
    except ValueError as e:
        raise e

    return booking


def print_booking(booking: Booking) -> None:
    print_divider()
    print(f"\nBooking for {len(booking.traveler_bookings)} traveler(s)")
    print("Prices:\n")

    for traveler_booking in booking.traveler_bookings:
        msg = f"{traveler_booking.age_category.name} " \
              f"{traveler_booking.ski_category.name} " \
              f"{traveler_booking.price} SEK "

        if traveler_booking.price_reduced > 0:
            msg += f"reduction {traveler_booking.price_reduced} SEK"
        print(msg)

    print(f"\nTotal Price: {booking.total_price} SEK\n")
