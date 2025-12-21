from clients.db_client import AgeCategory
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
