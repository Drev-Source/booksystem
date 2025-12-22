import mysql.connector

from pydantic import BaseModel
from typing import Any


class AgeCategory(BaseModel):
    id: int
    name: str
    minage: int
    maxage: int


class SkiCategory(BaseModel):
    id: int
    name: str


class PriceEntry(BaseModel):
    skiid: int
    agecatid: int
    price: int


class SqlQueryException(Exception): ...


class DatabaseConnectionException(Exception): ...


class DatabaseClient:
    def __init__(self, host: str = "localhost", user: str = "test", password: str = "tester", database: str = "ski_db") -> None:
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        except mysql.connector.Error as e:
            print(e)
            raise DatabaseConnectionException("Failed connecting to database")

        self.cursor = self.connection.cursor()


    def execute_query(self, query: str) -> Any:
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            raise SqlQueryException(f"Something went wrong executing query {query}")

        return self.cursor.fetchall()


    def close(self) -> None:
        self.cursor.close()
        self.connection.close()


    def fetch_price_list(self) -> list[PriceEntry]:
        stored_prices = self.execute_query(
            "SELECT skiid, agecatid, price FROM prices " \
            "WHERE skiid IS NOT NULL " \
            "AND agecatid IS NOT NULL " \
            "AND price IS NOT NULL;"
            )

        prices: list[PriceEntry] = []
        for entry in stored_prices:
            if not len(entry) == 3:
                print(f"Missing fields in entry {entry}, skipping")
                continue
            if not all(isinstance(i, int) for i in entry):
                print(f"Invalid type in entry {entry}, skipping")
                continue

            prices.append(PriceEntry(skiid=int(entry[0]), agecatid=int(entry[1]), price=int(entry[2])))

        return prices

    def fetch_age_categories(self) -> dict[int, AgeCategory]:
        stored_age_categories = self.execute_query(
            "SELECT id, name, minage, maxage FROM age_category " \
            "WHERE id IS NOT NULL " \
            "AND name IS NOT NULL " \
            "AND minage IS NOT NULL " \
            "AND maxage IS NOT NULL;"
            )

        age_categories: dict[int, AgeCategory] = {}
        for entry in stored_age_categories:
            if not len(entry) == 4:
                print(f"Missing fields in entry {entry}, skipping")
                continue

            if isinstance(entry[0], int) and isinstance(entry[2], int) and isinstance(entry[3], int):
                age_categories[int(entry[0])] = AgeCategory(id=int(entry[0]), name=entry[1], minage=int(entry[2]), maxage=int(entry[3]))
            else:
                print(f"Invalid type in entry {entry}, skipping")

        return age_categories


    def fetch_ski_categories(self) -> dict[int, SkiCategory]:
        stored_ski_categories = self.execute_query(
            "SELECT id, name FROM ski_category " \
            "WHERE id IS NOT NULL " \
            "AND name IS NOT NULL;"
            )

        ski_categories: dict[int, SkiCategory] = {}
        for entry in stored_ski_categories:
            if not len(entry) == 2:
                print(f"Missing fields in entry {entry}, skipping")
                continue

            if isinstance(entry[0], int):
                ski_categories[int(entry[0])] = SkiCategory(id=entry[0], name=entry[1])
            else:
                print(f"Invalid type in entry {entry}, skipping")

        return ski_categories
