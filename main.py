import uvicorn
from fastapi import FastAPI
import psycopg2

import os
import psycopg2


POSTGRES_HOST = "localhost"  # os.environ["POSTGRES_HOST"]
POSTGRES_DB = "db"  # os.environ["POSTGRES_DB"]
POSTGRES_USER = "user"  # os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = "password"  # os.environ["POSTGRES_PASSWORD"]

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)

PKEY = "key"

app = FastAPI()


@app.get("/")
def read_root():
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT count(*) FROM people
                """
            )

            row = curs.fetchone()
            count = row[0]

            return {"count": count}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
