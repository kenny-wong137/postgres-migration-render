import os
import time
from typing import NamedTuple

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


class TaskDefinition(NamedTuple):
    task_id: str
    input: int


class TaskResult(NamedTuple):
    task_id: str
    output: int


def load_task_definitions():
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT task_id, input
                FROM tasks
                WHERE output IS NULL
                """
            )

            rows = curs.fetchall()
            task_definitions = [
                TaskDefinition(task_id=row[0], input=row[1])
                for row in rows
            ]
            return task_definitions


def save_task_result(task_result):
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                UPDATE tasks
                SET output = %s
                WHERE task_id = %s
                """,
                (task_result.output, task_result.task_id)
            )

        print("Computed:", task_result)


def compute(task_definition):
    return TaskResult(
        task_id=task_definition.task_id,
        output=(task_definition.input * 2)
    )


def main():
    while True:
        task_definitions = load_task_definitions()
        for task_definition in task_definitions:
            task_result = compute(task_definition)
            save_task_result(task_result)

        time.sleep(5)


if __name__ == "__main__":
    main()
