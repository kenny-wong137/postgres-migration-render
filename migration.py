import os
import psycopg2


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

PKEY = "key"


def get_current_version():
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                CREATE TABLE IF NOT EXISTS version (
                  pkey TEXT NOT NULL,
                  version INTEGER NOT NULL
                )
                """
            )

            # If no version record exists, create one with version as zero
            curs.execute(
                """
                INSERT INTO version VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (PKEY, 0)
            )

            curs.execute(
                """
                SELECT version FROM version
                WHERE pkey = %s
                """,
                (PKEY,)
            )

            row = curs.fetchone()
            version = row[0]

            print("Current version:", version)

            return version


def set_version(version):
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                UPDATE version
                SET version = %s
                WHERE pkey = %s
                """,
                (version, PKEY)
            )

            print("Updated to version:", version)


def migrate_v0_to_v1():
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                CREATE TABLE people (
                  name TEXT NOT NULL
                )
                """
            )


def migrate_v1_to_v2():
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                ALTER TABLE people
                ADD COLUMN age INTEGER
                """
            )


VERSIONS_TO_MIGRATION_FUNCTIONS = {
    0: migrate_v0_to_v1,
    1: migrate_v1_to_v2
}


def main():
    version = get_current_version()

    while version in VERSIONS_TO_MIGRATION_FUNCTIONS:
        migration_function = VERSIONS_TO_MIGRATION_FUNCTIONS[version]
        migration_function()

        version += 1
        set_version(version)


if __name__ == "__main__":
    main()
