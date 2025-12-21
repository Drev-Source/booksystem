from db_client import AgeCategory, PriceEntry, SkiCategory
from yr_client import YRWeatherData


def print_divider() -> None:
    print("="*80)


def print_menu() -> None:
    print_divider()
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
    print_divider()
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


def print_age_categories(age_categories: dict[int, AgeCategory]) -> None:
    print_divider()
    print("Age Categories:")
    for age_category_id, age_category in age_categories.items():
        print(f"{age_category_id}: {age_category.name} ({age_category.minage}-{age_category.maxage})")
    print("\n")


def print_ski_categories(ski_categories: dict[int, SkiCategory]) -> None:
    print_divider()
    print("Ski Categories:")
    for ski_category_id, ski_category in ski_categories.items():
        print(f"{ski_category_id}: {ski_category.name}")
    print("\n")


def print_yr_licenses() -> None:
    print("\nWeather data provided by YR.no under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.")
    print("See https://creativecommons.org/licenses/by/4.0/ for more information.\n")


#TODO Add units for weather data
def print_weather_data(current_weather: YRWeatherData) -> None:
    print_divider()
    print(f"Weather is:")
    print(f"Air pressure: {current_weather.air_pressure_at_sea_level}")
    print(f"Air temperature: {current_weather.air_temperature}")
    print(f"Cloud area fraction: {current_weather.cloud_area_fraction}")
    print(f"Relative humidity: {current_weather.relative_humidity}")
    print(f"Wind direction: {current_weather.wind_from_direction}")
    print(f"Wind speed: {current_weather.wind_speed}")
    print_yr_licenses()
