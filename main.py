import uvicorn
from fastapi import FastAPI
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


@app.post("/tasks/{task_id}")
def create_task(task_id: str):
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                INSERT INTO tasks VALUES (%s, %s, %s)
                """,
                (task_id, 1, None)
            )


@app.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT output
                FROM tasks
                WHERE task_id = %s
                """,
                (task_id,)
            )

            row = curs.fetchone()
            return row[0]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
