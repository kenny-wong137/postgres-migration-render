import os
import psycopg2
import random


POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)


def create_person():
    name = "name-" + str(random.randint(0, 100000))
    age = 50

    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                INSERT INTO people VALUES (%s, %s)
                """,
                (name, age)
            )


if __name__ == "__main__":
    create_person()
