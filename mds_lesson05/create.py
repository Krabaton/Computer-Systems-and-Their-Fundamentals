import logging
from psycopg2 import DatabaseError

from connect import create_connect


def create_table(conn, sql_stmt: str):
    c = conn.cursor()
    try:
        c.execute(sql_stmt)
        conn.commit()
    except DatabaseError as err:
        logging.error(f"Database error: {err}")
        conn.rollback()
    finally:
        c.close()


if __name__ == "__main__":
    sql_stmt = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name varchar(120),
        email varchar(120),
        password varchar(120),
        age smallint CHECK (age > 0 AND age < 150)
    )
    """

    try:
        with create_connect() as conn:
            create_table(conn, sql_stmt)
    except RuntimeError as err:
        logging.error(f"Runtime error: {err}")
