from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    pk INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    age INTEGER NOT NULL
                )
            """
            )
