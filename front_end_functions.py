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
    age_categories: dict[int, AgeCategory],
    ski_categories: dict[int, SkiCategory],
) -> None:
    print("\nPrice List:\n")

    for skiid in ski_categories.keys():
        ski_category = ski_categories[skiid]
        column_name = f"{ski_category.name}"
        print(column_name)

        filtered_prices = [price for price in prices if price.skiid == skiid]
        for entry in filtered_prices:
            age_cat = age_categories.get(entry.agecatid)
            if age_cat:
                row = f"{age_cat.name} ({age_cat.minage}-{age_cat.maxage})"
                while len(row) < 20:
                    row += " "
                row += f"|   Pris: {entry.price} SEK"
                print("-"*len(row))
                print(row)
        print("\n")


def list_latest_prices() -> None:
    # Fetch latest data
    db_client = DatabaseClient()
    prices = db_client.fetch_price_list()
    age_categories = db_client.fetch_age_categories()
    ski_categories = db_client.fetch_ski_categories()
    db_client.close()

    list_prices(prices, age_categories, ski_categories)


def print_age_categories(age_categories: dict[int, AgeCategory]) -> None:
    print("Age Categories:")
    for age_category_id, age_category in age_categories.items():
        print(f"{age_category_id}: {age_category.name} ({age_category.minage}-{age_category.maxage})")
    print("\n")


def print_ski_categories(ski_categories: dict[int, SkiCategory]) -> None:
    print("Ski Categories:")
    for ski_category_id, ski_category in ski_categories.items():
        print(f"{ski_category_id}: {ski_category.name}")
    print("\n")
