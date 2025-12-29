# Booksystem
This is a project for a small CLI booksystem program. Allowing you to create a booking using information stored in a MySQL database.
You can also see weather forecast and the program will reduce the price for oldest and youngest age group.

## Setup
The project has been tested and developed in an WSL environment (windows subsystem linux). Recommendation for smoothest setup is to be in an
Linux environment as the following guidelines have been written for that environment.

### Install MySQL
If you have not setup the MySQL beforehand you can follow this microsoft learn guide on how to install MySQL on a linux distrubtion running on WSL.

>https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database


### Default client configuration
For the smoothest start and use of program you can configure the database name and test user accordingly or pass the desired user and database name or change the default params.

The defualt params configured in the db_client is:
>* host: str = "localhost"
>* user: str = "test"
>* password: str = "tester"
>* database: str = "ski_db"

### Import sql scheme
Using the ski_db.sql file in the docs folder, you can setup the database used in testing and running the program.

> `mysql -u <username> -p <databasename> < <filename.sql>`

### Install project requirements
A requirements.txt is provided to install packages that is used within the program. To install the packages execute following command in root of project:

>`pip install -r requirements.txt`

## Usage
The project is written in python and is recommended to run in a python virtual environment (venv).

To run the program use (python is expected to be installed):

> `python main.py`

## Code
### clients
Clients used to communicate with external services.
* **db_client.py**: Client to connect and query MySQL database.
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