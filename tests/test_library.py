import unittest
from src.library import *

class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Initialize and seed the database"""
        exec_sql_file("db-kjv7359/src/init_db.sql")
        exec_sql_file("db-kjv7359/tests/seed_test_db.sql")

    def test_verify_rows(self):
        """Check the number of rows for each table"""
        self.assertEqual(countRows("users"), 4)
        self.assertEqual(countRows("books"), 7)
        self.assertEqual(countRows("checkout"), 10)
        self.assertEqual(countRows("reserve"), 0)

    def test_list_user_books_empty(self):
        """Ensure listUserBooks() returns an empty list for Art"""
        books = listUserBooks("Art Garfunkel")
        self.assertEqual(books, [])

    def test_list_user_books_multiple(self):
        """Ensure listUserBooks() returns the correct sorted items for Jackie"""
        books = listUserBooks("Jackie Gleason")
        self.assertEqual(books, ['Dynasty', 'Mort', 'The Woman in White'])

    def test_list_all_checked_out_books(self):
        """Check the output of listAllCheckedOutBooks()"""
        name_book_tuples = listAllCheckedOutBooks()
        self.assertEqual(name_book_tuples, [
            ('Ada Lovelace',   'Dynasty'),
            ('Ada Lovelace',   'The Secret History'),
            ('Jackie Gleason', 'Dynasty'),
            ('Jackie Gleason', 'Mort'),
            ('Jackie Gleason', 'The Woman in White'),
            ('Mary Shelley',   'Dynasty'),
            ('Mary Shelley',   'Mort'),
            ('Mary Shelley',   'The Making of a Story'),
            ('Mary Shelley',   'The Midnight Disease'),
            ('Mary Shelley',   'The Woman in White'),
        ])

    def test_list_nonfiction_quantity_books(self):
        """Check the output of listTypeBooks() for a given type"""
        title_quantity_tuples = listTypeBooks("nonfiction")
        self.assertEqual(title_quantity_tuples, [
            ('Dynasty', 3),
            ('The Making of a Story', 5),
            ('The Midnight Disease', 10),
        ])

    def test_list_books_date(self):
        """Check the output of listBooksByDate()"""
        title_date_tuples = listBooksByDate()
        self.assertEqual(title_date_tuples, [
            ('Frankenstein',           1818),
            ('The Woman in White',     1860),
            ('The Secret History',     1992),
            ('Mort',                   1998),
            ('The Midnight Disease',   2004),
            ('The Making of a Story',  2009),
            ('Dynasty',                2015),
        ])

    def test_list_table_names(self):
        """Ensure listTableNames() returns the names of all the tables"""
        tables = listTableNames()
        self.assertEqual(tables, [
            'books',
            'checkout',
            'reserve',
            'users'
        ])

    def test_book_type_totals(self):
        """Ensure countType() returns correct types and counts"""
        type_count_tuples = countType()
        self.assertEqual(type_count_tuples,
            [('fiction', 4), ('nonfiction', 3)]
        )

    def test_create_user(self):
        """Ensure users are created and displayed"""
        name = 'Christopher Marlowe'
        phone = '585-1234-567'
        email = 'speare@gmail.com'
        createUser(name, phone, email)

        name2 = 'Francis Bacon'
        phone2 = '777-888-9999'
        email2 = 'notkevin@gmail.com'
        createUser(name2, phone2, email2)

        self.assertEqual(getUser(name), (name, phone, email))
        self.assertEqual(getUser(name2), (name2, phone2, email2))

    def test_book_search_deactivate_user(self):
        """Ensure user can be deactivated"""
        title = 'The Last Man'
        user = 'Mary Shelley'
        self.assertEqual(searchBook(title), 0)
        deactivateUser(user)
        self.assertEqual(isActive(user), False)

    def test_return_book(self):
        """Ensure books can be returned and date is tracked"""
        user = 'Art Garfunkel'
        title = 'Frankenstein'
        checkoutBook(user, title, '2024-01-01')
        returnBook(user, title, '2024-01-04')
        self.assertEqual(daysCheckedOut(user, title), 3)

    def test_count_remaining_copies(self):
        """Ensure getRemainingCopies() returns the correct amount"""
        title = 'Mort'
        self.assertEqual(getRemainingCopies(title), 1)

    def test_checkout_book_available(self):
        """Ensure a book can be checked out if it's available"""
        user = 'Ada Lovelace'
        title = 'Mort'
        date = '2024-01-01'
        checkoutBook(user, title, date)
        self.assertEqual(isCheckedOut(user, title), 1)

    def test_checkout_book_unavailable(self):
        """Ensure a book can't be checked out if no copies remain"""
        user = 'Ada Lovelace'
        title = 'Dynasty'
        date = '2024-01-01'
        with self.assertRaises(ValueError):
            # this should raise an error
            checkoutBook(user, title, date)

    def test_list_checkout_log(self):
        """Check the output of listCheckoutLog()"""
        self.assertEqual(listCheckoutLog(), [
            ('fiction',     'Donna Tartt',      'The Secret History',    'Ada Lovelace',     '2024-02-03', None, 3),
            ('fiction',     'Terry Pratchett',  'Mort',                  'Jackie Gleason',   '2024-02-03', None, 1),
            ('fiction',     'Terry Pratchett',  'Mort',                  'Mary Shelley',     '2024-02-03', None, 1),
            ('fiction',     'Wilkie Collins',   'The Woman in White',    'Jackie Gleason',   '2024-02-03', None, 6),
            ('fiction',     'Wilkie Collins',   'The Woman in White',    'Mary Shelley',     '2024-02-03', None, 6),
            ('nonfiction',  'Alice Flaherty',   'The Midnight Disease',  'Mary Shelley',     '2024-02-03', None, 9),
            ('nonfiction',  'Alice LaPlante',   'The Making of a Story', 'Mary Shelley',     '2024-02-03', None, 4),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'Ada Lovelace',     '2024-02-03', None, 0),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'Jackie Gleason',   '2024-02-03', None, 0),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'Mary Shelley',     '2024-02-03', None, 0),
        ])

    def test_reserve_book_with_copies(self):
        """Ensure a book cannot be reserved if copies remain"""
        user = 'Jackie Gleason'
        title = 'Mort'
        with self.assertRaises(ValueError):
            # this should raise an error
            reserveBook(user, title)

    def test_reserve_book_success(self):
        """Ensure a book can be reserved under normal circumstances"""
        user = 'Jackie Gleason'
        title = 'Dynasty'
        reserveBook(user, title)
        self.assertEqual(isReserved(title), 1)

    def test_load_data_books(self):
        """Ensure .csv data is successfully inserted into the database"""
        path = "db-kjv7359/tests/library.csv"
        full_path = os.path.join(os.path.dirname(__file__), f'../../{path}')
        loadDataBooks(full_path)
        self.assertEqual(countRows('books'), 26)
