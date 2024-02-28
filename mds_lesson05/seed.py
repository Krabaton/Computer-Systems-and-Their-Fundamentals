import logging
from random import randint

from faker import Faker
from psycopg2 import DatabaseError

from connect import create_connect

fake = Faker("uk_UA")
COUNT = 3000


def insert_data(conn, sql_stmt: str):
    c = conn.cursor()
    try:
        for _ in range(COUNT):
            name = fake.name()
            email = fake.email()
            password = fake.password()
            age = randint(1, 95)
            c.execute(sql_stmt, (name, email, password, age))
        conn.commit()
    except DatabaseError as err:
        logging.error(f"Database error: {err}")
        conn.rollback()
    finally:
        c.close()


if __name__ == "__main__":
    sql_stmt = """
    INSERT INTO users (name, email, password, age) VALUES (%s, %s, %s, %s)
    """

    try:
        with create_connect() as conn:
            insert_data(conn, sql_stmt)
    except RuntimeError as err:
        logging.error(f"Runtime error: {err}")
