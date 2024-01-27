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

def unpack(x):
    return [y for y, in x]

def listUserBooks(username):
    books = exec_get_all(
        """SELECT books.title FROM books
            INNER JOIN book_status ON books.id=book_status.book_id
            INNER JOIN users ON users.id=book_status.user_id
        WHERE users.name = %s
            ORDER BY title ASC""", (username,))
    return unpack(books)

def listAllCheckedOutBooks():
    books = exec_get_all(
        """SELECT users.name, books.title FROM books
            INNER JOIN book_status ON books.id=book_status.book_id
            INNER JOIN users ON users.id=book_status.user_id
        ORDER BY users.name ASC, books.title ASC""")
    return books

def listTypeBooks(book_type):
    books = exec_get_all(
        """SELECT books.title, book_availability.count FROM books
            INNER JOIN book_availability ON books.id=book_availability.book_id
        WHERE books.type = %s
        ORDER BY books.title ASC""", (book_type,))
    return books
