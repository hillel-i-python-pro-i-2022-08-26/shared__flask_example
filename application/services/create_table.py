from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                pk INTEGER NOT NULL PRIMARY KEY,
                name VARCHAR NOT NULL,
                age INTEGER NOT NULL
            )
        """
        )
