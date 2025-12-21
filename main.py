#!/usr/bin/env python3
from booking import (
    Booking,
    print_booking,
    start_booking
)
from utility.exceptions import AbortBookingException
from front_end import (
    print_menu,
    print_weather_data,
    list_latest_prices
)
from clients.yr_client import YRClient


def main() -> None:
    print_menu()
    current_booking: Booking | None = None
    while True:
        try:
            line = input("> ").strip()
        except EOFError as e:
            print(repr(e))
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()
        
        if cmd in ("exit", "quit", "0"):
            print("Bye.")
            break

        elif cmd == "1": # List prices
            list_latest_prices()

        elif cmd == "2": # Show weather
            yr_client = YRClient()
            weather = yr_client.get_current_weather()
            print_weather_data(weather)

        elif cmd == "3": # Create booking
            try:
                new_booking = start_booking()
                if new_booking:
                    current_booking = new_booking
                    print("Successfully created a new booking:")
            except AbortBookingException as e:
                print(repr(e))
            except ValueError as e:
                print(repr(e))
                print("Recovering value error, continue program")

        elif cmd == "4": # Show booking
            if current_booking:
                print_booking(current_booking)
            else:
                print("There is no current booking.")
        else:
            print(f"Unknown command: {cmd}.")

        print_menu()


if __name__ == "__main__":
    main()
