from db_client import AgeCategory, SkiCategory


def print_age_categories(ageCategories: dict[int, AgeCategory]) -> None:
    print("Age Categories:")
    for agecatid, agecat in ageCategories.items():
        print(f"{agecatid}: {agecat.name} ({agecat.minage}-{agecat.maxage})")
    print("\n")


def print_ski_categories(skiCategories: dict[int, SkiCategory]) -> None:
    print("Ski Categories:")
    for skicatid, skicat in skiCategories.items():
        print(f"{skicatid}: {skicat.name}")
    print("\n")


def get_age_category_id(age: int, ageCategories: dict[int, AgeCategory]) -> int | None:
    # What if the age fits multiple categories?
    # What if the age fits no category?
    for agecatid, agecat in ageCategories.items():
        if agecat.minage <= age <= agecat.maxage:
            return agecatid
    print("No age category found for this age. Self destructing booking process.\n")
    return None


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


def ask_for_age(ageCategories: dict[int, AgeCategory]) -> int | None:
    print_age_categories(ageCategories)
    prompt = "Please enter the age of traveler:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) >= 0:
        age_category = get_age_category_id(int(line), ageCategories)
        return age_category
    else:
        print(f"Invalid input: {line}, please enter age within listed ranges")
        return ask_for_age(ageCategories)


def ask_for_ski_category(skiCategories: dict[int, SkiCategory]) -> int | None:
    print_ski_categories(skiCategories)
    prompt = "Please enter the ski category ID from the list above:"
    line = wait_for_user_input(prompt)

    if line is None:
        return None
    elif line.isdigit() and int(line) > 0:
        return int(line)
    else:
        print(f"Invalid input: {line}, please enter a listed number")
        return ask_for_ski_category(skiCategories)
