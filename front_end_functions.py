from db_client import AgeCategory, DatabaseClient, PriceEntry, SkiCategory


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


def list_latest_prices() -> None:
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    ageCategories = db_client.fetch_age_categories()
    skiCategories = db_client.fetch_ski_categories()
    db_client.close()

    list_prices(prices, ageCategories, skiCategories)
