from src.swen344_db_utils import *
from psycopg2 import sql

def rebuildTables():
    """Reinitialize a clean database with sample data"""
    exec_sql_file("db-kjv7359/src/library.sql")

def countRows(table):
    """Returns the number of rows in the given table"""
    count, = exec_get_one(
        sql.SQL("SELECT count(*) FROM {table}").format(table=sql.Identifier(table))
    )
    return count

def unpack(x):
    """Convert a list of one-tuples to a list of plain values"""
    return [y for y, in x]

def listUserBooks(username):
    """Returns the list of book titles the given user has checked out"""
    books = exec_get_all(
        """SELECT books.title FROM books
            INNER JOIN book_status ON books.id=book_status.book_id
            INNER JOIN users ON users.id=book_status.user_id
        WHERE users.name = %s
        ORDER BY title ASC""", (username,))
    return unpack(books)

def listAllCheckedOutBooks():
    """Get the list of books checked out by all users
    
    Returns a list of (user, book title) pairs."""
    books = exec_get_all(
        """SELECT users.name, books.title FROM books
            INNER JOIN book_status ON books.id=book_status.book_id
            INNER JOIN users ON users.id=book_status.user_id
        ORDER BY users.name ASC, books.title ASC""")
    return books

def listTypeBooks(book_type):
    """Get the list of books with the given type

    Returns a list of (book title, book total) pairs."""
    books = exec_get_all(
        """SELECT books.title, book_availability.count FROM books
            INNER JOIN book_availability ON books.id=book_availability.book_id
        WHERE books.type = %s
        ORDER BY books.title ASC""", (book_type,))
    return books

def listBooksByDate():
    """Get the list of all books ordered by publication date"""
    books = exec_get_all(
        """SELECT books.title, books.pub_date FROM books
        ORDER BY books.pub_date ASC, books.title ASC""")
    return books

def listTableNames():
    """Get the list of the names of all tables"""
    tables = exec_get_all(
        """SELECT tablename FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename ASC""")
    return unpack(tables)

def countType():
    """Count the number of books of each type

    Returns a list of (book type, count) pairs."""
    books = exec_get_all(
        """SELECT books.type,
            COUNT(*) AS type_count
        FROM books
        GROUP BY books.type
        ORDER BY books.type ASC""")
    return books
