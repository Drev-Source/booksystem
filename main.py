#!/usr/bin/env python3
from db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory


def print_menu():
    print("\nPlease enter the number of your choice\n")
    print("Menu:")
    print("\"1\" list prices")
    print("\"2\" create booking")
    print("\"0\" exit\n")


def list_prices(
        prices: list[PriceEntry],
        ageCategories: dict[int, AgeCategory],
        skiCategories: dict[int, SkiCategory],
    ):
    print("\nPrice List:\n")

    column_ids = skiCategories.keys()

    for col_id in column_ids:
        ski_cat = skiCategories[col_id]
        column = f"{ski_cat.name}"
        print(column)

        sorted_price_entries = [price_entry for price_entry in prices if price_entry.skiid == col_id]
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


def print_age_categories(ageCategories: dict[int, AgeCategory]):
    print("Age Categories:")
    for agecatid, agecat in ageCategories.items():
        print(f"{agecatid}: {agecat.name} ({agecat.minage}-{agecat.maxage})")
    print("\n")


def ask_for_age_category(ageCategories: dict[int, AgeCategory]) -> int | None:
    print_age_categories(ageCategories)
    prompt = "Please enter the age category ID from the list above:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) > 0:
        return int(line)
    else:
        print(f"Invalid input: {line}, please enter a listed number")
        return ask_for_age_category(ageCategories)


def print_ski_categories(skiCategories: dict[int, SkiCategory]):
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


def create_booking(
        prices: list[PriceEntry],
        ageCategories: dict[int, AgeCategory],
        skiCategories: dict[int, SkiCategory],
    ) -> None:
    travelers = ask_for_amount_of_travelers()
    total_price = 0
    if not travelers:
        return

    for traveler in range(1, travelers+1):
        print(f"Traveler {traveler}/{travelers}:")
        age_category = ask_for_age_category(ageCategories)
        if not age_category:
            return

        print(f"Traveler {traveler} is {ageCategories[age_category].name}\n")
        list_prices(prices, ageCategories, skiCategories)
        ski_category = ask_for_ski_category(skiCategories)
        if not ski_category:
            return

        print(f"Selected {skiCategories[ski_category].name} for traveler {traveler}\n")

        traveler_price = [price for price in prices if price.agecatid == age_category and price.skiid == ski_category]
        if traveler_price:
            print(f"Price for this combination is {traveler_price[0].price} SEK.\n")
            total_price += traveler_price[0].price
        else:
            print(f"No price found for this combination {ageCategories[age_category].name} and {skiCategories[ski_category].name}.")

    print(f"Total price: {total_price} SEK\n")


def main():
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    ageCategories = db_client.fetch_age_categories()
    skiCategories = db_client.fetch_ski_categories()
    db_client.close()

    print_menu()
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
        args = parts[1:]

        if cmd in ('exit', 'quit', '0'):
            print('Bye.')
            break
        elif cmd == '1':
            list_prices(prices, ageCategories, skiCategories)
        elif cmd == '2':
            create_booking(prices, ageCategories, skiCategories)
        else:
            print(f"Unknown command: {cmd}.")

        print_menu()


if __name__ == '__main__':
    main()