from src.swen344_db_utils import *
from psycopg2 import sql
import csv


def countRows(table):
    """
    Count the rows in the given table

    Args:
        table: name of the table

    Returns:
        the number of rows in `table`
    """
    count, = exec_get_one(
        sql.SQL("SELECT COUNT(*) FROM {table}").format(table=sql.Identifier(table))
    )
    return count


def _unpack(x):
    """Convert a list of one-tuples to a list of plain values"""
    return [y for y, in x]


def listUserBooks(user):
    """
    List the books checked out by a user

    Args:
        user: name of the user

    Returns:
        a sorted list of book titles
    """
    books = exec_get_all("""
        SELECT books.title FROM books
            INNER JOIN checkout ON books.id = checkout.book_id
            INNER JOIN users    ON users.id = checkout.user_id
        WHERE users.name = %s
        ORDER BY title ASC
    """, (user,))
    return _unpack(books)


def listAllCheckedOutBooks():
    """
    List the books checked out by all users
    
    Returns:
        a sorted list of (user, book title) pairs
    """
    books = exec_get_all("""
        SELECT users.name, books.title FROM books
            INNER JOIN checkout ON books.id = checkout.book_id
            INNER JOIN users    ON users.id = checkout.user_id
        WHERE checkout.is_returned = FALSE
        ORDER BY users.name ASC, books.title ASC
    """)
    return books


def listTypeBooks(book_type):
    """
    List the books with a given type
    
    Args:
        book_type: the type of book

    Returns:
        a sorted list of (book title, quantity) pairs
    """
    books = exec_get_all("""
        SELECT books.title, books.copies FROM books
        WHERE books.type = %s
        ORDER BY books.title ASC
    """, (book_type,))
    return books


def listBooksByDate():
    """
    List all books in order of publication date

    Returns:
        a list of (book title, publication date) pairs sorted by publication date and title
    """
    books = exec_get_all("""
        SELECT books.title, books.pub_date FROM books
        ORDER BY books.pub_date ASC, books.title ASC
    """)
    return books


def listTableNames():
    """
    List all tables in the database

    Returns:
        a sorted list of table names
    """
    tables = exec_get_all("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename ASC
    """)
    return _unpack(tables)


def countType():
    """
    Count the number of books of each type

    Returns:
        a sorted list of (book type, count) pairs
    """
    books = exec_get_all("""
        SELECT books.type, COUNT(*) FROM books
        GROUP BY books.type
        ORDER BY books.type ASC
    """)
    return books


def getUser(name):
    """
    Get information about a user
    
    Args:
        name: the name of a user

    Returns:
        a tuple of (name, phone number, email address)
    """
    user = exec_get_one("""
        SELECT users.name, users.phone, users.email FROM users
        WHERE users.name = %s
    """, (name,))
    return user


def createUser(name, phone, email):
    """
    Add a new user to the database

    Args:
        name:  the user's name
        phone: the user's phone number
        email: the user's email address
    """
    exec_commit("""
        INSERT INTO users(name, phone, email)
        VALUES (%s, %s, %s)
    """, (name, phone, email))


def deactivateUser(name):
    """
    Deactivate a user's account

    Args:
        name: the name of a user
    """
    exec_commit("""
        UPDATE users SET active = FALSE
        WHERE users.name = %s
    """, (name,))


def isActive(name):
    """
    Check if an account is active

    Args:
        name: the name of a user

    Returns:
        True if the user is active, False otherwise
    """
    is_active, = exec_get_one("""
        SELECT users.active FROM users
        WHERE users.name = %s
    """, (name,))
    return is_active


def getRemainingCopies(title):
    """
    Get the number of copies of a book that haven't been checked out

    Args:
        title: the title of a book

    Returns:
        the remaining number of copies
    """
    total, = exec_get_one("""
        SELECT books.copies FROM books
        WHERE books.title = %s
    """, (title,))
    checkout_total, = exec_get_one("""
        SELECT COUNT(books.title) FROM books
            INNER JOIN checkout ON books.id = checkout.book_id
        WHERE books.title = %s AND is_returned = FALSE
    """, (title,))
    return total - checkout_total


def isCheckedOut(user, title):
    """
    Check if a given user has a given book checked out

    Args:
        user:  the name of a user
        title: the name of a book

    Returns:
        True if the user has the book checked out, False otherwise
    """
    exists, = exec_get_one("""
        SELECT COUNT(books.title) FROM books
            INNER JOIN checkout ON books.id = checkout.book_id
            INNER JOIN users    ON users.id = checkout.user_id
        WHERE users.name = %s AND books.title = %s
    """, (user, title))
    return exists


def checkoutBook(user, title, date):
    """
    Check out the given book on behalf of the user

    Args:
        user:  the user's name
        title: the book's title
        date:  the date the user checked out the book

    Raises:
        ValueError: there are no copies left to check out
    """
    if getRemainingCopies(title) == 0:
        raise ValueError('No copies left to check out.')
    exec_commit("""
        INSERT INTO checkout(user_id, book_id)
        SELECT
            (SELECT users.id FROM users
            WHERE users.name = %s),
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (user, title))
    exec_commit("""
        UPDATE checkout SET checkout_date = %s
        WHERE user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (date, user, title))


def returnBook(user, title, date):
    """
    Return a book and keep the history

    Args:
        user:  the user's name
        title: the book's title
        date:  the date the user returned the book
    """
    exec_commit("""
        UPDATE checkout
            SET is_returned = TRUE, return_date = %s
        WHERE user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (date, user, title))


def daysCheckedOut(user, title):
    """
    Get the duration a book has been checked out for

    Args:
        user:  the user's name
        title: the book's title

    Returns:
        the number of days the book has been checked out
    """
    date_diff, = exec_get_one("""
        SELECT checkout.return_date - checkout.checkout_date AS date_diff
        FROM checkout
        WHERE user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (user, title))
    return date_diff


def listCheckoutLog():
    """
    List all books that were ever checked out
    
    Returns:
        A list of tuples of (book type, book author, book title, user name, remaining copies)
    """
    books = exec_get_all("""
        SELECT books.type, books.author, books.title, users.name,
        TO_CHAR(checkout.checkout_date, 'YYYY-MM-DD'),
        TO_CHAR(checkout.return_date, 'YYYY-MM-DD')
        FROM books
            INNER JOIN checkout ON books.id = checkout.book_id
            INNER JOIN users    ON users.id = checkout.user_id
        ORDER BY books.type ASC, books.author ASC, users.name ASC
    """)
    return [(ty, a, ti, *x, getRemainingCopies(ti)) for ty, a, ti, *x in books]


def isReserved(title):
    """
    Check if a book is reserved

    Args:
        title: the title of a book

    Returns:
        True if the book is reserved, False otherwise
    """
    exists, = exec_get_one("""
        SELECT COUNT(books.title) FROM reserve
            INNER JOIN books ON books.id = reserve.book_id
        WHERE books.title = %s
    """, (title,))
    return exists


def reserveBook(user, title):
    """
    Reserve a book on behalf of a user

    Args:
        user:  the user's name
        title: the book's title

    Raises:
        ValueError: there are still copies of the book left
    """
    if getRemainingCopies(title) != 0:
        raise ValueError('Copies of this book still remain.')

    exec_commit("""
        INSERT INTO reserve (user_id, book_id)
        SELECT
            (SELECT users.id FROM users
            WHERE users.name = %s),
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (user, title))


def searchBook(title):
    """
    Check if a book is in the database

    Args:
        title: the title of a book

    Returns:
        True if the book is in the database, False otherwise
    """
    exists, = exec_get_one("""
        SELECT COUNT(books.title) FROM books
        WHERE books.title = %s
    """, (title,))
    return exists


def loadDataBooks(path):
    """
    Insert books into the database from a table on disk

    Args:
        path: the path to a .csv file
    """
    with connect() as conn, open(path, newline='') as csvfile:
        cur = conn.cursor()
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for title, author, summary, type_, sub_type, copies in csvreader:
            if type_.lower() == 'fiction':
                type_ = 'fiction'
            elif type_.lower() == 'non-fiction' or 'nonfiction':
                type_ = 'nonfiction'
            cur.execute("""
                INSERT INTO books(title, author, summary, type, sub_type, copies)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, author, summary, type_, sub_type, copies))
        conn.commit()
