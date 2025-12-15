from typing import Any
import mysql.connector

class DatabaseClient:
    def __init__(self, host: str = "localhost", user: str = "test", password: str = "tester", database: str = "ski_db") -> None:
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str) -> Any:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()
