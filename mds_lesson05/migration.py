import logging

from faker import Faker
from psycopg2 import DatabaseError

from connect import create_connect

fake = Faker("uk_UA")
COUNT = 3000


def migration(conn, sql_stmt: str):
    c = conn.cursor()
    try:
        c.execute(sql_stmt)
        conn.commit()
    except DatabaseError as err:
        logging.error(f"Database error: {err}")
        conn.rollback()
    finally:
        c.close()


def update_data(conn, sql_stmt: str):
    c = conn.cursor()
    try:
        for i in range(COUNT):
            phone = fake.phone_number()
            c.execute(sql_stmt, (phone, i + 1))
        conn.commit()
    except DatabaseError as err:
        logging.error(f"Database error: {err}")
        conn.rollback()
    finally:
        c.close()


if __name__ == "__main__":
    sql_stmt = """
    ALTER TABLE users ADD COLUMN IF NOT EXISTS phone varchar(30);
    """
    sql_stmt_udate = """
    UPDATE users SET phone = %s WHERE id = %s;
    """

    try:
        with create_connect() as conn:
            migration(conn, sql_stmt)
            update_data(conn, sql_stmt_udate)
    except RuntimeError as err:
        logging.error(f"Runtime error: {err}")
