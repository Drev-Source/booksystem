# Booksystem
This is a project for a small CLI booksystem program.
Allowing you to create a booking using information stored in a MYSQL database. You can also see weather forecast and the program will reduce the price for oldest and youngest age group.

## Usage
The project is written in python and is recommended to run in a python virtual environment (venv).

A requirements.txt is provided to install packages that is used within the program. To install the packages execute following command in root of project:

>`pip install -r requirements.txt`

Then run the program using:

> `python main.py`

## Code
### clients
Clients used to communicate with external services.
* **db_client.py**: Client to connect and query MYSQL database.
* **yr_client.py**: Client to query API provided by YR.no.

### utility
General functions to be used throughout the program.
* **economy.py**: Functionality to calculate prices and price reductions.
* **exceptions.py**: Custom exceptions
* **utlity.py**: General purpose functions, mainly related to processing age categories
* **time.py**: Time and date functionality

### root
* **main.py**: Main program
* **booking.py**: Functionality and classes for creating a booking.
* **user_input.py**: Functions used to prompt user for information.
* **front_end.py**: Functionality to visualize information to the user.

## Docs
CODEOWNER file and a TODO file with tasks for future implementation and improvements.