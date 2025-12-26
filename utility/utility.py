import hashlib

from clients.db_client import AgeCategory


def find_lowest_and_highest_age_group(age_categories: dict[int, AgeCategory]) -> tuple[AgeCategory]:
    if not age_categories:
        raise ValueError("Age categories can't be empty")

    lowest = list(age_categories.values())[0]
    highest = list(age_categories.values())[0]

    for age_category in age_categories.values():
        # Prioritize lowest min age and then lowest max age
        if lowest.minage >= age_category.minage:
            if lowest.maxage > age_category.minage:
                lowest = age_category

        # Prioritize highest max age and then highest low age
        if highest.maxage <= age_category.maxage:
            if highest.minage < age_category.minage:
                highest = age_category

    return lowest, highest


# What if the age fits multiple categories?
# What if the age fits no category?
# Should we try to choose closest category?
def get_age_category_id(age: int, age_categories: dict[int, AgeCategory]) -> int | None:
    for age_category_id, age_category in age_categories.items():
        if age_category.minage <= age <= age_category.maxage:
            return age_category_id

    return None


def hash_content(content: str):
        return hashlib.sha256(content.encode()).hexdigest()
