from db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory
from front_end_functions import list_prices, print_weather_data
from pydantic import BaseModel
from user_input_functions import ask_for_age, ask_for_amount_of_travelers, ask_for_ski_category
from yr_client import YRClient, YRWeatherData


class TravelerBooking(BaseModel):
    age_category: AgeCategory
    ski_category: SkiCategory
    price: int
    price_reduced: int


class Booking(BaseModel):
    traveler_bookings: list[TravelerBooking]
    total_price: int


def list_latest_prices() -> None:
    # Fetch latest data
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    age_categories = db_client.fetch_age_categories()
    ski_categories = db_client.fetch_ski_categories()
    db_client.close()

    list_prices(prices, age_categories, ski_categories)


def find_lowest_and_highest_age_group(age_categories: dict[int, AgeCategory]) -> tuple[AgeCategory, AgeCategory]:
    if not age_categories:
        raise ValueError("Age categories can't be empty")

    lowest = list(age_categories.values())[0] # Prioritize lowest min age and then lowest max age
    highest = list(age_categories.values())[0] # Prioritize highest max age and then highest low age

    for age_category in age_categories.values():
        if lowest.minage >= age_category.minage:
            if lowest.maxage > age_category.minage:
                lowest = age_category

        if highest.maxage <= age_category.maxage:
            if highest.minage < age_category.minage:
                highest = age_category

    return lowest, highest


def get_youngest_weather_price_reduction(current_weather: YRWeatherData) -> float:
    if current_weather.air_temperature < 14:
        return 0
    else:
        return 1


def get_oldest_weather_price_reduction(current_weather: YRWeatherData) -> float:
    if current_weather.air_temperature >= 18:
        return 0.6
    else:
        return 1


def get_price_reduction(age_category_id: int, age_categories: dict[int, AgeCategory]) -> float:
    if not age_categories:
        return 1

    yr_client = YRClient()
    current_weather = yr_client.get_current_weather()

    if not current_weather:
        return 1

    print_weather_data(current_weather)
    youngest_group, oldest_group = find_lowest_and_highest_age_group(age_categories)

    if age_category_id == youngest_group.id:
        return get_youngest_weather_price_reduction(current_weather)
    elif age_category_id == oldest_group.id:
        return get_oldest_weather_price_reduction(current_weather)
    else:
        return 1


def calculate_traveler_price(
    prices: list[PriceEntry],
    age_category_id: int,
    ski_category_id: int,
    age_categories: dict[int, AgeCategory],
) -> tuple[int, bool]:
    
    for record in prices:
        if record.agecatid == age_category_id and record.skiid == ski_category_id:
            reduction = get_price_reduction(age_category_id, age_categories)
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
        msg = f"{traveler_booking.age_category.name} " \
              f"{traveler_booking.ski_category.name} " \
              f"{traveler_booking.price} SEK "

        if traveler_booking.price_reduced > 0:
            msg += f"reduction {traveler_booking.price_reduced} SEK"
        print(msg)

    print(f"\nTotal Price: {booking.total_price} SEK\n")
