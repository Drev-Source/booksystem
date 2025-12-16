#!/usr/bin/env python3
from db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory
from booking import Booking, TravelerBooking


def print_menu() -> None:
    print("\nPlease enter the number of your choice\n")
    print("Menu:")
    print("\"1\" List prices")
    print("\"2\" Create booking")
    print("\"3\" Show current booking")
    print("\"0\" Exit\n")


def list_prices(
    prices: list[PriceEntry],
    ageCategories: dict[int, AgeCategory],
    skiCategories: dict[int, SkiCategory],
) -> None:
    print("\nPrice List:\n")

    column_ids = skiCategories.keys()

    for col_id in column_ids:
        ski_cat = skiCategories[col_id]
        column = f"{ski_cat.name}"
        print(column)

        sorted_price_entries = [price for price in prices if price.skiid == col_id]
        for sorted_entry in sorted_price_entries:
            age_cat = ageCategories.get(sorted_entry.agecatid)
            if age_cat:
                row = f"{age_cat.name} ({age_cat.minage}-{age_cat.maxage})"
                while len(row) < 20:
                    row += " "
                row += f"|   Pris: {sorted_entry.price} SEK"
                print("-"*len(row))
                print(row)
        print("\n")


def wait_for_user_input(prompt: str) -> str:
    print(prompt)
    print("You can type 'exit' or 'quit' to leave.")
    while True:
        try:
            line = input('> ').strip()
        except EOFError:
            print()
            break

        if not line:
            continue
        elif line.lower() in ('exit', 'quit'):
            print("Cancelling")
            return None

        return line


def ask_for_amount_of_travelers() -> int | None:
    prompt = "Please enter the amount of travelers:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) > 0:
        print(f"\nNumber of travelers: {int(line)}\n")
        return int(line)
    else:
        print(f"Invalid input: {line}, please enter a listed number")
        return ask_for_amount_of_travelers()


def print_age_categories(ageCategories: dict[int, AgeCategory]) -> None:
    print("Age Categories:")
    for agecatid, agecat in ageCategories.items():
        print(f"{agecatid}: {agecat.name} ({agecat.minage}-{agecat.maxage})")
    print("\n")


def get_age_category_id(age: int, ageCategories: dict[int, AgeCategory]) -> int | None:
    # What if the age fits multiple categories?
    # What if the age fits no category?
    for agecatid, agecat in ageCategories.items():
        if agecat.minage <= age <= agecat.maxage:
            return agecatid
    print("No age category found for this age. Self destructing booking process.\n")
    return None


def ask_for_age(ageCategories: dict[int, AgeCategory]) -> int | None:
    print_age_categories(ageCategories)
    prompt = "Please enter the age of traveler:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) >= 0:
        age_category = get_age_category_id(int(line), ageCategories)
        return age_category
    else:
        print(f"Invalid input: {line}, please enter age within listed ranges")
        return ask_for_age(ageCategories)


def print_ski_categories(skiCategories: dict[int, SkiCategory]) -> None:
    print("Ski Categories:")
    for skicatid, skicat in skiCategories.items():
        print(f"{skicatid}: {skicat.name}")
    print("\n")


def ask_for_ski_category(skiCategories: dict[int, SkiCategory]) -> int | None:
    print_ski_categories(skiCategories)
    prompt = "Please enter the ski category ID from the list above:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) > 0:
        return int(line)
    else:
        print(f"Invalid input: {line}, please enter a listed number")
        return ask_for_ski_category(skiCategories)


def print_booking(booking: Booking) -> None:
    print(f"\nBooking for {len(booking.traveler_bookings)} traveler(s)")
    print("Prices:\n")
    for traveler_booking in booking.traveler_bookings:
        print(f"{traveler_booking.age_category.name} {traveler_booking.ski_category.name} {traveler_booking.price} SEK")
    print(f"\nTotal Price: {booking.total_price} SEK\n")


def calculate_traveler_price(prices: list[PriceEntry], age_category_id: int, ski_category_id: int) -> int | None:
    for record in prices:
        if record.agecatid == age_category_id and record.skiid == ski_category_id:
            return record.price
    return None


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


def create_booking(
    travelers: int,
    prices: list[PriceEntry],
    ageCategories: dict[int, AgeCategory],
    skiCategories: dict[int, SkiCategory],
) -> Booking | None:
    traveler_bookings: list[TravelerBooking] = []
    for traveler in range(1, travelers+1):
        print(f"Traveler {traveler}/{travelers}:")

        age_category_id = ask_for_age(ageCategories)
        if not age_category_id:
            return

        subset_age_categories = {k: ageCategories[k] for k in ageCategories if k == age_category_id}
        list_prices(prices, subset_age_categories, skiCategories)

        ski_category_id = ask_for_ski_category(skiCategories)
        if not ski_category_id:
            return

        traveler_bookings.append(
            TravelerBooking(
                age_category=ageCategories[age_category_id],
                ski_category=skiCategories[ski_category_id],
                price=calculate_traveler_price(prices, age_category_id, ski_category_id),
            )
            )

    total_price = calculate_booking_price(traveler_bookings)
    return Booking(traveler_bookings=traveler_bookings, total_price=total_price)


def start_booking() -> Booking:
    # Fetch latest data
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    ageCategories = db_client.fetch_age_categories()
    skiCategories = db_client.fetch_ski_categories()
    db_client.close()

    list_prices(prices, ageCategories, skiCategories)

    travelers = ask_for_amount_of_travelers()
    if not travelers:
        return

    return create_booking(travelers, prices, ageCategories, skiCategories)
    

def main() -> None:
    print_menu()
    current_booking: Booking | None = None
    while True:
        try:
            line = input('> ').strip()
        except EOFError:
            print()
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()
        
        if cmd in ('exit', 'quit', '0'):
            print('Bye.')
            break
        elif cmd == '1':
            # Fetch latest data and list prices
            db_client = DatabaseClient()
            prices = db_client.fetch_price_list()
            ageCategories = db_client.fetch_age_categories()
            skiCategories = db_client.fetch_ski_categories()
            db_client.close()

            list_prices(prices, ageCategories, skiCategories)
        elif cmd == '2':
            booking = start_booking()
            if booking:
                current_booking = booking
                print("Successfully created a new booking:")
        elif cmd == '3':
            if current_booking:
                print_booking(current_booking)
            else:
                print("There is no current booking.")
        else:
            print(f"Unknown command: {cmd}.")

        print_menu()


if __name__ == '__main__':
    main()