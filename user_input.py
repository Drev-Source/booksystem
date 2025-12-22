from clients.db_client import AgeCategory, SkiCategory
from utility.exceptions import AbortException, RetryException
from utility.utility import get_age_category_id


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
        print(e)
        return ask_for_amount_of_travelers()


def ask_for_age(age_categories: dict[int, AgeCategory]) -> int:
    prompt = "Please enter the age of traveler:"
    line = wait_for_user_input(prompt)

    try:
        if line.isdigit() and int(line) >= 0:
            age_category = get_age_category_id(int(line), age_categories)
            if not age_category:
                raise RetryException(f"Invalid input: {int(line)}, please enter age within listed ranges")
            return age_category
        else:
            raise RetryException(f"Invalid input: {line}, please enter age within listed ranges")
    except RetryException as e:
        print(e)
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
        print(e)
        return ask_for_ski_category(ski_categories)
