from db_client import AgeCategory, SkiCategory
from front_end_functions import print_age_categories, print_ski_categories


def get_age_category_id(age: int, age_categories: dict[int, AgeCategory]) -> int | None:
    #TODO What if the age fits multiple categories?
    #TODO What if the age fits no category?
    for age_category_id, age_category in age_categories.items():
        if age_category.minage <= age <= age_category.maxage:
            return age_category_id
    print("No age category found for this age. Self destructing booking process.\n")
    return None


#TODO Could probably do a better fault handling using exceptions here and not None returns
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


#TODO Could probably do a better fault handling using exceptions here and not None returns
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


#TODO Could probably do a better fault handling using exceptions here and not None returns
def ask_for_age(age_categories: dict[int, AgeCategory]) -> int | None:
    print_age_categories(age_categories)
    prompt = "Please enter the age of traveler:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) >= 0:
        age_category = get_age_category_id(int(line), age_categories)
        return age_category
    else:
        print(f"Invalid input: {line}, please enter age within listed ranges")
        return ask_for_age(age_categories)


#TODO Could probably do a better fault handling using exceptions here and not None returns
def ask_for_ski_category(ski_categories: dict[int, SkiCategory]) -> int | None:
    print_ski_categories(ski_categories)
    prompt = "Please enter the ski category ID from the list above:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) > 0:
        return int(line)
    else:
        print(f"Invalid input: {line}, please enter a listed number")
        return ask_for_ski_category(ski_categories)
