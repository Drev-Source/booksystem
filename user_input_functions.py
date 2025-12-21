from db_client import AgeCategory, SkiCategory
from exceptions import AbortException, RetryException


def get_age_category_id(age: int, age_categories: dict[int, AgeCategory]) -> int | None:
    for age_category_id, age_category in age_categories.items():
        if age_category.minage <= age <= age_category.maxage:
            return age_category_id

    # What if the age fits multiple categories?
    # What if the age fits no category?
    # Should we try to choose closest category?
    raise RetryException(f"Invalid input: {age}, please enter age within listed ranges")


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
            raise AbortException("Cancelling")

        return line


def ask_for_amount_of_travelers() -> int:
    prompt = "Please enter the amount of travelers:"
    line = wait_for_user_input(prompt)

    try:
        if line.isdigit() and int(line) > 0:
            print(f"\nNumber of travelers: {int(line)}\n")
            return int(line)
        else:
            raise RetryException(f"Invalid input: {line}, please enter a number larger than 0")
    except RetryException as e:
        print(repr(e))
        return ask_for_amount_of_travelers()


def ask_for_age(age_categories: dict[int, AgeCategory]) -> int:
    prompt = "Please enter the age of traveler:"
    line = wait_for_user_input(prompt)

    try:
        if line.isdigit() and int(line) >= 0:
            age_category = get_age_category_id(int(line), age_categories)
            return age_category
        else:
            raise RetryException(f"Invalid input: {line}, please enter age within listed ranges")
    except RetryException as e:
        print(repr(e))
        return ask_for_age(age_categories)


def ask_for_ski_category(ski_categories: dict[int, SkiCategory]) -> int:
    prompt = "Please enter the ski category ID from the list above:"
    line = wait_for_user_input(prompt)

    try:
        if line.isdigit() and int(line) > 0:
            if int(line) not in ski_categories.keys():
                raise RetryException(f"Invalid input: {line}, please enter a listed number")
            
            return int(line)
        else:
            raise RetryException(f"Invalid input: {line}, please enter a listed number")
    except RetryException as e:
        print(repr(e))
        return ask_for_ski_category(ski_categories)
