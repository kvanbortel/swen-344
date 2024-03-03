import os
from .swen344_db_utils import *

def rebuild_tables():
    exec_sql_file('src/db/schema.sql')
    exec_sql_file('src/db/test_data.sql')

def list_examples():
    """This is an example. Please remove from your code before REST1 deadline.
    DB layer call for listing all rows of our example.
    """
    return exec_get_all('SELECT id, foo FROM example_table')

def getUsers():
    """
    DB layer call for listing all relevant rows of users table

    Returns:
        A list of tuples of (user id, name, phone, email)"""
    return exec_get_all('SELECT id, name, phone, email FROM users')

def getBooks():
    """
    List all of the books in all libraries by library name and title

    Returns:
        A list of tuples of (library name, title, copies)
    """
    books = exec_get_all("""
        SELECT libraries.location, books.title, inventory.copies FROM inventory
            INNER JOIN libraries ON libraries.id = inventory.library_id
            INNER JOIN books     ON books.id = inventory.book_id
        ORDER BY libraries.location ASC, books.title ASC
    """)
    return books
