from src.swen344_db_utils import *
from psycopg2 import sql

def rebuildTables():
    """Recreate the tables to initialize the db"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS example_table
    """
    create_sql = """
        CREATE TABLE example_table(
            example_col VARCHAR(40)
        )
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def countRows(table):
    count, = exec_get_one(
        sql.SQL("SELECT count(*) FROM {table}").format(table=sql.Identifier(table))
    )
    return count

def listUserBooks(username):
    result = []
    books, = exec_get_one(
        "SELECT users.items FROM users WHERE users.name = %s", (username,))
    if books:
        for book in books:
            title, = exec_get_one(
                "SELECT books.title FROM books INNER JOIN users ON books.id=%s", (book,)
            )
            result.append(title)
    return result
