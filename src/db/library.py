import os
from .swen344_db_utils import *
import hashlib
from flask_restful import Resource, reqparse, request
import json
import base64

def rebuild_tables():
    exec_sql_file('src/db/schema.sql')
    exec_sql_file('src/db/test_data.sql')

def getUsers():
    """
    DB layer call for listing all relevant rows of users table

    Returns:
        A list of tuples of (user id, name, phone, email)"""
    return exec_get_all('SELECT id, name, phone, email FROM users')

def isActive(name):
    """Check if an account is active

    Args:
        name: name of a user

    Returns:
        True if the user is active, False otherwise
    """
    is_active, = exec_get_one("""
        SELECT users.active FROM users
        WHERE users.name = %s
    """, (name,))
    return is_active

def hashPassword(password):
    """Hash the given password"""
    hashed_password = hashlib.sha512(password.encode())
    return hashed_password.digest()

def getRemainingCopies(title, library):
    """
    Get the number of copies of a book that haven't been checked out

    Args:
        title:   the title of a book
        library: the library to get the book from

    Returns:
        the remaining number of copies
    """
    total, = exec_get_one("""
        SELECT inventory.copies FROM inventory
            INNER JOIN books     ON books.id = inventory.book_id
            INNER JOIN libraries ON libraries.id = inventory.library_id
        WHERE books.title = %s
    """, (title,))
    checkout_total, = exec_get_one("""
        SELECT COUNT(books.title) FROM books
            INNER JOIN checkout  ON books.id = checkout.book_id
            INNER JOIN libraries ON libraries.id = checkout.library_id
        WHERE libraries.location = %s AND books.title = %s AND is_returned = FALSE
    """, (library, title))
    return total - checkout_total

def checkoutBook(user, title, library, date):
    """
    Check out the given book on behalf of the user

    Args:
        user:     the user's name
        title:    the book's title
        library:  the library the book is from
        date:     the date the user checked out the book

    Raises:
        ValueError: there are no copies left to check out
    """
    if getRemainingCopies(title, library) == 0:
        raise ValueError('No copies left to check out.')
    exec_commit("""
        INSERT INTO checkout(user_id, book_id, library_id)
        SELECT
            (SELECT users.id FROM users
            WHERE users.name = %s),
            (SELECT books.id FROM books
            WHERE books.title = %s),
            (SELECT libraries.id FROM libraries
            WHERE libraries.location = %s)
    """, (user, title, library))
    exec_commit("""
        UPDATE checkout SET checkout_date = %s
        WHERE library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.location = %s)
        AND user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (date, library, user, title))

def isReserved(title, library):
    """
    Check if a book is reserved

    Args:
        title:   the title of a book
        library: the library the book is from

    Returns:
        True if the book is reserved, False otherwise
    """
    exists, = exec_get_one("""
        SELECT COUNT(books.title) FROM reserve
            INNER JOIN books ON books.id = reserve.book_id
        WHERE reserve.library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.location = %s)
        AND books.title = %s
    """, (library, title))
    return exists

def reserveBook(user, title, library):
    """
    Reserve a book on behalf of a user

    Args:
        user:    the user's name
        title:   the book's title
        library: the library to retrieve the book from

    Raises:
        ValueError: there are still copies of the book left
    """
    if getRemainingCopies(title, library) != 0:
        raise ValueError('Copies of this book still remain.')

    exec_commit("""
        INSERT INTO reserve (user_id, book_id, library_id)
        SELECT
            (SELECT users.id FROM users
            WHERE users.name = %s),
            (SELECT books.id FROM books
            WHERE books.title = %s),
            (SELECT libraries.id FROM libraries
            WHERE libraries.location = %s)
    """, (user, title, library))

def isAuthenticated():
    """Authenticate a user's session key"""
    parser = reqparse.RequestParser()
    parser.add_argument('session_key', type=str)
    args = parser.parse_args()
    session_key = args.session_key
    session_key = base64.b64decode(session_key)

    _isAuthenticated, = exec_get_one("""
        SELECT EXISTS
            (SELECT users.id FROM users
            WHERE users.session_key = %s)
    """, (session_key,))
    return _isAuthenticated
