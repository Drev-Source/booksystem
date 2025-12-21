from clients.db_client import AgeCategory, PriceEntry
from utility.utility import find_lowest_and_highest_age_group


def get_young_price_reduction(temperature: float) -> float:
    if temperature < 14:
        return 0
    else:
        return 1


def get_old_price_reduction(temperature: float) -> float:
    if temperature >= 18:
        return 0.6
    else:
        return 1


def get_price_reduction(
    age_category_id: int,
    age_categories: dict[int, AgeCategory],
    temperature: float
) -> float:
    if not age_categories:
        return 1

    youngest_group, oldest_group = find_lowest_and_highest_age_group(age_categories)

    if age_category_id == youngest_group.id:
        return get_young_price_reduction(temperature)
    elif age_category_id == oldest_group.id:
        return get_old_price_reduction(temperature)
    else:
        return 1
    

def calculate_traveler_price(
    prices: list[PriceEntry],
    age_category_id: int,
    ski_category_id: int,
    age_categories: dict[int, AgeCategory],
    air_temperature: float | None,
) -> tuple[int, bool]:
    for record in prices:
        if record.agecatid == age_category_id and record.skiid == ski_category_id:
            if air_temperature:
                reduction = get_price_reduction(age_category_id,
                                                age_categories,
                                                air_temperature
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
