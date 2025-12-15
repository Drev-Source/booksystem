#!/usr/bin/env python3
from db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory


def print_menu():
    print("Menu:")
    print("\"1\" list prices")
    print("\"2\" create booking")
    print("\"0\" exit")


def print_price_list(
        prices: list[PriceEntry],
        ageCategories: dict[int, AgeCategory],
        skiCategories: dict[int, SkiCategory],
    ):
    print("Price List:")
    print("\n\n")

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

        print("\n\n")


def print_booking_menu():
    print("Booking menu is not yet implemented.")


def main():
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    ageCategories = db_client.fetch_age_categories()
    skiCategories = db_client.fetch_ski_categories()
    db_client.close()

    print("Please enter the number of your choice or \"help\" for assistance")
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
            print_price_list(prices, ageCategories, skiCategories)
        elif cmd == '2':
            print_booking_menu()
        else:
            print(f"Unknown command: {cmd}.")

        print_menu()


if __name__ == '__main__':
    main()