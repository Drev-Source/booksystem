#!/usr/bin/env python3
from booking import (
    Booking,
    get_oldest_weather_price_reduction,
    get_youngest_weather_price_reduction,
    list_latest_prices,
    print_booking,
    start_booking
    )
from exceptions import AbortBookingException
from front_end_functions import print_menu, print_weather_data
from yr_client import YRClient


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
            reduction_young = get_youngest_weather_price_reduction(weather.data)
            reduction_old = get_oldest_weather_price_reduction(weather.data)
            print_weather_data(weather, reduction_young, reduction_old)

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
