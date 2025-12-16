#!/usr/bin/env python3
from booking import Booking, list_latest_prices, print_booking, start_booking
from front_end_functions import print_menu


#Should use try except for fault handling here instead of Nones
def main() -> None:
    print_menu()
    current_booking: Booking | None = None
    while True:
        try:
            line = input('> ').strip()
        except EOFError:
            print()
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()
        
        if cmd in ('exit', 'quit', '0'):
            print('Bye.')
            break
        elif cmd == '1':
            list_latest_prices()
        elif cmd == '2':
            booking = start_booking()
            if booking:
                current_booking = booking
                print("Successfully created a new booking:")
        elif cmd == '3':
            if current_booking:
                print_booking(current_booking)
            else:
                print("There is no current booking.")
        else:
            print(f"Unknown command: {cmd}.")

        print_menu()


if __name__ == '__main__':
    main()