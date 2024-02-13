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


def listTypeBooks(book_type, library):
    """
    List the books with a given type at a library
    
    Args:
        book_type: the type of book
        library:   the library the books are from

    Returns:
        a sorted list of (book title, quantity) pairs
    """
    books = exec_get_all("""
        SELECT books.title, inventory.copies FROM books
            INNER JOIN inventory     ON books.id = inventory.book_id
            INNER JOIN libraries ON libraries.id = inventory.library_id
        WHERE books.type = %s
        AND libraries.name = %s
        ORDER BY books.title ASC
    """, (book_type, library))
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


def hasOverdueBook(user, date):
    """
    Check if a user has an overdue book

    Args:
        user: name of the user
        date: date user wants to check out a new book

    Returns:
        True if the user has an overdue book, False otherwise
    """
    has_overdue_book, = exec_get_one("""
        SELECT COUNT(users.name) FROM checkout
            INNER JOIN users ON users.id = checkout.user_id
        WHERE users.name = %s
        AND checkout.is_returned = FALSE
        AND (%s - checkout.checkout_date) >= 14
    """, (user, date)) # a book is overdue when it reaches 14 days checked out
    return has_overdue_book


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
        WHERE libraries.name = %s AND books.title = %s AND is_returned = FALSE
    """, (library, title))
    return total - checkout_total


def isCheckedOut(user, title, library):
    """
    Check if a given user has a given book checked out

    Args:
        user:    the name of a user
        title:   the name of a book
        library: the name of the library the book is from

    Returns:
        True if the user has the book checked out, False otherwise
    """
    exists, = exec_get_one("""
        SELECT COUNT(books.title) FROM books
            INNER JOIN checkout  ON books.id = checkout.book_id
            INNER JOIN users     ON users.id = checkout.user_id
            INNER JOIN libraries ON libraries.id = checkout.library_id
        WHERE users.name = %s AND books.title = %s
            AND libraries.name = %s
    """, (user, title, library))
    return exists


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
    if hasOverdueBook(user, date) == 1:
        raise ValueError('User has an overdue book.')
    exec_commit("""
        INSERT INTO checkout(user_id, book_id, library_id)
        SELECT
            (SELECT users.id FROM users
            WHERE users.name = %s),
            (SELECT books.id FROM books
            WHERE books.title = %s),
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
    """, (user, title, library))
    exec_commit("""
        UPDATE checkout SET checkout_date = %s
        WHERE library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
        AND user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (date, library, user, title))


def returnBook(user, title, library, date):
    """
    Return a book and keep the history

    Args:
        user:    the user's name
        title:   the book's title
        library: the library the book is from
        date:    the date the user returned the book
    """
    exec_commit("""
        UPDATE checkout
            SET is_returned = TRUE, return_date = %s
        WHERE library_id = 
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
        AND user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (date, library, user, title))


def daysCheckedOut(user, title, library):
    """
    Get the duration a book has been checked out for

    Args:
        user:    the user's name
        title:   the book's title
        library: the name of the library the book is from

    Returns:
        the number of days the book has been checked out
    """
    date_diff, = exec_get_one("""
        SELECT checkout.return_date - checkout.checkout_date AS date_diff
        FROM checkout
        WHERE library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
        AND user_id =
            (SELECT users.id FROM users
            WHERE users.name = %s)
        AND book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
    """, (library, user, title))
    return date_diff


def listCheckoutLog():
    """
    List all books that were ever checked out
    
    Returns:
        A list of tuples of (book type, book author, book title, user name, library name, checkout date,
        return date, remaining copies)
    """
    books = exec_get_all("""
        SELECT books.type, books.author, books.title, users.name, libraries.name,
        TO_CHAR(checkout.checkout_date, 'YYYY-MM-DD'),
        TO_CHAR(checkout.return_date, 'YYYY-MM-DD')
        FROM books
            INNER JOIN checkout  ON books.id = checkout.book_id
            INNER JOIN users     ON users.id = checkout.user_id
            INNER JOIN libraries ON libraries.id = checkout.library_id
        ORDER BY books.type ASC, books.author ASC, users.name ASC
    """)
    return [(ty, a, ti, us, li, *x, getRemainingCopies(ti, li)) for ty, a, ti, us, li, *x in books]


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
            WHERE libraries.name = %s)
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
            WHERE libraries.name = %s)
    """, (user, title, library))


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


def getLendingHistory(user):
    """
    Return the lending history for a certian user

    Args:
        user: the name of the user

    Returns:
        A list of tuples of (book type, book author, book title, library name, checkout date,
        return date, remaining copies)
    """
    books = exec_get_all("""
        SELECT books.type, books.author, books.title, libraries.name,
        TO_CHAR(checkout.checkout_date, 'YYYY-MM-DD'),
        TO_CHAR(checkout.return_date, 'YYYY-MM-DD')
        FROM books
            INNER JOIN checkout  ON books.id = checkout.book_id
            INNER JOIN users     ON users.id = checkout.user_id
            INNER JOIN libraries ON libraries.id = checkout.library_id
        WHERE users.name = %s
        ORDER BY books.type ASC, books.author ASC, libraries.name ASC
    """, (user,))
    return [(ty, a, ti, li, *x, getRemainingCopies(ti, li)) for ty, a, ti, li, *x in books]


def loadDataBooks(path, library):
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
                WITH inserted_id AS (
                    INSERT INTO books (title, author, summary, type, sub_type)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                )
                INSERT INTO inventory (library_id, book_id, copies)
                VALUES
                    (
                    (SELECT libraries.id FROM libraries
                        WHERE libraries.name = %s),
                    (SELECT id FROM inserted_id),
                    %s
                    )
            """, (title, author, summary, type_, sub_type, library, copies))
        conn.commit()


def addNewBookToLibrary(title, library):
    """
    Add a new book to a library

    Args:
        title:   the title of the book to add
        library: the name of the library to add the book to
    """
    exec_commit("""
        INSERT INTO inventory (library_id, book_id)
        VALUES
            (
            (SELECT libraries.id FROM libraries
                WHERE libraries.name = %s),
            (SELECT books.id FROM books
                WHERE books.title = %s)
            )
    """, (library, title))


def bookInLibrary(title, library):
    """
    Check if a given book is in a given library

    Args:
        title:   the name of the book
        library: the name of the library

    Returns:
        True if the book is in the library, False otherwise
    """
    in_library, = exec_get_one("""
        SELECT COUNT(inventory.book_id) FROM inventory
            INNER JOIN books     ON books.id = inventory.book_id
            INNER JOIN libraries ON libraries.id = inventory.library_id
        WHERE books.title = %s
        AND libraries.name = %s
    """, (title, library))
    return in_library


def addCopiesToLibrary(title, author, book_type, library, copies):
    """
    If the book is not in the inventory, add it.
    If it is not in the library, add it.
    Add the number of new copies to the library's stock.

    Args:
        title:     the name of the book
        author:    the name of the author
        book_type: the type of book (fiction or nonfiction)
        library:   the name of the library to add copies to
        copies:    the number of copies to add to the library
    """
    if searchBook(title) == 0:
        addBook(title, author, book_type)

    if bookInLibrary(title, library) == 0:
        addNewBookToLibrary(title, library)

    exec_commit("""
        UPDATE inventory SET copies = (copies + %s)
        WHERE book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
        AND library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
    """, (copies, title, library))
 

def addBook(title, author, book_type):
    """
    Add a book to the inventory

    Args:
        title:     the name of the book
        author:    the name of the book's author
        book_type: the type of book (fiction or nonfiction)
    """
    exec_commit("""
        INSERT INTO books (title, author, type)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (title, author, book_type))


def getCopiesFromLibrary(title, library):
    """
    Get the number of copies of a book at a library

    Args:
        title:   the name of the book
        library: the name of the library

    Returns:
        The number of copies of the book
    """
    copies, = exec_get_one("""
        SELECT copies FROM inventory
        WHERE book_id =
            (SELECT books.id FROM books
            WHERE books.title = %s)
        AND library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
    """, (title, library))
    return copies


def listOverdueHistory():
    """
    List the log of previously overdue books by user

    Returns:
       A list of tuples of (user name, book title, checkout date, return date, days overdue)
       ordered by the user's name and the amount of days the book was checked out
    """
    books = exec_get_all("""
        SELECT users.name, books.title,
        TO_CHAR(checkout.checkout_date, 'YYYY-MM-DD'),
        TO_CHAR(checkout.return_date, 'YYYY-MM-DD'),
        (checkout.return_date - checkout.checkout_date) AS date_diff
        FROM books
            INNER JOIN checkout ON books.id = checkout.book_id
            INNER JOIN users    ON users.id = checkout.user_id
        WHERE (checkout.return_date - checkout.checkout_date) >= 14
        ORDER BY users.name ASC, date_diff DESC
    """)
    return books


def listAllBooksLibrary(library):
    """
    List all of the books in a library by title

    Args:
        library: the name of the library

    Returns:
        A list of tuples of (book title, copies)
    """
    books = exec_get_all("""
        SELECT books.title, inventory.copies FROM books
            INNER JOIN inventory ON books.id = inventory.book_id
        WHERE library_id =
            (SELECT libraries.id FROM libraries
            WHERE libraries.name = %s)
        ORDER BY books.title
    """, (library,))
    return books


def listAllBooks():
    """
    List all of the books in all libraries by library name and title

    Returns:
        A list of tuples of (library name, title, copies)
    """
    books = exec_get_all("""
        SELECT libraries.name, books.title, inventory.copies FROM inventory
            INNER JOIN libraries ON libraries.id = inventory.library_id
            INNER JOIN books     ON books.id = inventory.book_id
        ORDER BY libraries.name ASC, books.title ASC
    """)
    return books
