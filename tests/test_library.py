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
        book_type = 'nonfiction'
        library = 'test_library'
        title_quantity_tuples = listTypeBooks(book_type, library)
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
            'fairport',
            'henrietta',
            'penfield',
            'pittsford',
            'reserve',
            'test_library',
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
        library = 'test_library'
        checkoutBook(user, title, library, '2024-01-02')
        returnBook(user, title, library, '2024-01-05')
        self.assertEqual(daysCheckedOut(user, title, library), 3)

    def test_count_remaining_copies(self):
        """Ensure getRemainingCopies() returns the correct amount"""
        title = 'Mort'
        library = 'test_library'
        self.assertEqual(getRemainingCopies(title, library), 1)

    def test_checkout_book_available(self):
        """Ensure a book can be checked out if it's available"""
        user = 'Ada Lovelace'
        title = 'Mort'
        library = 'test_library'
        date = '2024-01-02'
        checkoutBook(user, title, library, date)
        self.assertEqual(isCheckedOut(user, title, library), 1)

    def test_checkout_book_unavailable(self):
        """Ensure a book can't be checked out if no copies remain"""
        user = 'Ada Lovelace'
        title = 'Dynasty'
        library = 'test_library'
        date = '2024-01-02'
        with self.assertRaises(ValueError):
            # this should raise an error
            checkoutBook(user, title, library, date)

    def test_checkout_book_overdue_14(self):
        """Ensure a book can't be checked out if user has an overdue book of 14 days"""
        user = 'Ada Lovelace'
        title = 'Dynasty'
        library = 'test_library'
        date = '2024-01-15'
        with self.assertRaises(ValueError):
            # this should raise an error
            checkoutBook(user, title, library, date)

    def test_list_checkout_log(self):
        """Check the output of listCheckoutLog()"""
        self.assertEqual(listCheckoutLog(), [
            ('fiction',     'Donna Tartt',      'The Secret History',    'Ada Lovelace',     'test_library', '2024-01-01', None, 3),
            ('fiction',     'Terry Pratchett',  'Mort',                  'Jackie Gleason',   'test_library', '2024-01-01', None, 1),
            ('fiction',     'Terry Pratchett',  'Mort',                  'Mary Shelley',     'test_library', '2024-01-01', None, 1),
            ('fiction',     'Wilkie Collins',   'The Woman in White',    'Jackie Gleason',   'test_library', '2024-01-01', None, 6),
            ('fiction',     'Wilkie Collins',   'The Woman in White',    'Mary Shelley',     'test_library', '2024-01-01', None, 6),
            ('nonfiction',  'Alice Flaherty',   'The Midnight Disease',  'Mary Shelley',     'test_library', '2024-01-01', None, 9),
            ('nonfiction',  'Alice LaPlante',   'The Making of a Story', 'Mary Shelley',     'test_library', '2024-01-01', None, 4),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'Ada Lovelace',     'test_library', '2024-01-01', None, 0),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'Jackie Gleason',   'test_library', '2024-01-01', None, 0),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'Mary Shelley',     'test_library', '2024-01-01', None, 0),
        ])

    def test_reserve_book_with_copies(self):
        """Ensure a book cannot be reserved if copies remain"""
        user = 'Jackie Gleason'
        title = 'Mort'
        library = 'test_library'
        with self.assertRaises(ValueError):
            # this should raise an error
            reserveBook(user, title, library)

    def test_reserve_book_success(self):
        """Ensure a book can be reserved under normal circumstances"""
        user = 'Jackie Gleason'
        title = 'Dynasty'
        library = 'test_library'
        reserveBook(user, title, library)
        self.assertEqual(isReserved(title, library), 1)

    def test_get_lending_history(self):
        """Ensure all lending history of a user is returned"""
        user = 'Mary Shelley'
        self.assertEqual(getLendingHistory(user), [
            ('fiction',     'Terry Pratchett',  'Mort',                  'test_library',     '2024-01-01', None, 1),
            ('fiction',     'Wilkie Collins',   'The Woman in White',    'test_library',     '2024-01-01', None, 6),
            ('nonfiction',  'Alice Flaherty',   'The Midnight Disease',  'test_library',     '2024-01-01', None, 9),
            ('nonfiction',  'Alice LaPlante',   'The Making of a Story', 'test_library',     '2024-01-01', None, 4),
            ('nonfiction',  'Tom Holland',      'Dynasty',               'test_library',     '2024-01-01', None, 0),
        ])

    def test_load_data_books(self):
        """Ensure .csv data is successfully inserted into the database"""
        path = "db-kjv7359/tests/library.csv"
        library = 'test_library'
        full_path = os.path.join(os.path.dirname(__file__), f'../../{path}')
        loadDataBooks(full_path, library)
        self.assertEqual(countRows('books'), 26)
        self.assertEqual(countRows('test_library'), 26)

    def test_overdue_books_scenario(self):
        """
        Ensure the same book can be added to different libraries, users can't check it out if they have an overdue
        book, and the librarian can list overdue history for all users
        """
        title = 'The Winds of Winter'
        author = 'George R.R. Martin'
        book_type = 'fiction'
        library1 = 'penfield'
        library2 = 'fairport'
        library3 = 'henrietta'
        library4 = 'pittsford'
        copies = 1
        addCopiesToLibrary(title, author, book_type, library1, copies)
        addCopiesToLibrary(title, author, book_type, library2, copies)
        addCopiesToLibrary(title, author, book_type, library3, copies)
        addCopiesToLibrary(title, author, book_type, library4, copies)
        self.assertEqual(searchBook(title), 1)
        self.assertEqual(bookInLibrary(title, library2), 1)

        user1 = 'Mary Shelley'
        checkout_date1 = '2024-01-02'
        return_date1 = '2024-01-10'
        checkoutBook(user1, title, library2, checkout_date1)
        returnBook(user1, title, library2, return_date1)

        user2 = 'Ada Lovelace'
        checkout_date2 = '2024-01-13'
        return_date2 = '2024-01-31'
        checkoutBook(user2, title, library2, checkout_date2)
        # return books currently checked out from test data:
        returnBook(user2, 'The Secret History', 'test_library', '2024-01-01')
        returnBook(user2, 'Dynasty', 'test_library', '2024-01-01')
        with self.assertRaises(ValueError):
            # this should raise an error
            checkoutBook(user2, 'Mort', library2, '2024-01-28')
        returnBook(user2, title, library2, return_date2)

        user3 = 'Jackie Gleason'
        checkout_date3 = '2024-03-01'
        return_date3 = '2024-03-31'
        # return books currently checked out from test data:
        returnBook(user3, 'Mort', 'test_library', '2024-01-01') 
        returnBook(user3, 'The Woman in White', 'test_library', '2024-01-01')
        returnBook(user3, 'Dynasty', 'test_library', '2024-01-01')
        checkoutBook(user3, title, library2, checkout_date3)
        returnBook(user3, title, library2, return_date3)
        
        self.assertEqual(listOverdueHistory(), [
            ('Ada Lovelace', 'The Winds of Winter', '2024-01-13', '2024-01-31', 18),
            ('Jackie Gleason', 'The Winds of Winter', '2024-03-01', '2024-03-31', 30),
        ])

    def test_add_additional_copies(self):
        """Ensure additional copies of a book can be added to a library"""
        title = 'The Winds of Winter'
        author = 'George R.R. Martin'
        book_type = 'fiction'
        library = 'fairport'
        copies = 1
        addCopiesToLibrary(title, author, book_type, library, copies)
        more_copies = 3
        addCopiesToLibrary(title, author, book_type, library, more_copies)
        self.assertEqual(getCopiesFromLibrary(title, library), 4)

    def test_add_book_to_multiple_libraries(self):
        """Ensure a book can be added to different libraries"""
        title = 'The Wines of Winter'
        author = 'WineExpress'
        book_type = 'nonfiction'
        library1 = 'pittsford'
        library2 = 'henrietta'
        copies = '2'
        addCopiesToLibrary(title, author, book_type, library1, copies)
        addCopiesToLibrary(title, author, book_type, library2, copies)
        self.assertEqual(getCopiesFromLibrary(title, library1), 2)
        self.assertEqual(getCopiesFromLibrary(title, library2), 2)

    def test_list_books_all_libraries(self):
        """Ensure all books can be listed by library and title"""
        self.assertEqual(listAllBooks(), [
            ('fairport', 'Dynasty', 2),
            ('fairport', 'Frankenstein', 1),
            ('fairport', 'Mort', 2),
            ('fairport', 'The Making of a Story', 3),
            ('fairport', 'The Midnight Disease', 8),
            ('fairport', 'The Secret History', 8),
            ('fairport', 'The Woman in White', 6),
            ('henrietta', 'Dynasty', 5),
            ('henrietta', 'Frankenstein', 1),
            ('henrietta', 'Mort', 2),
            ('henrietta', 'The Making of a Story', 3),
            ('henrietta', 'The Midnight Disease', 7),
            ('henrietta', 'The Secret History', 9),
            ('henrietta', 'The Woman in White', 4),
            ('penfield', 'Dynasty', 5),
            ('penfield', 'Frankenstein', 3),
            ('penfield', 'Mort', 1),
            ('penfield', 'The Making of a Story', 2),
            ('penfield', 'The Midnight Disease', 8),
            ('penfield', 'The Secret History', 2),
            ('penfield', 'The Woman in White', 6),
            ('pittsford', 'Dynasty', 2),
            ('pittsford', 'Frankenstein', 1),
            ('pittsford', 'Mort', 3),
            ('pittsford', 'The Making of a Story', 2),
            ('pittsford', 'The Midnight Disease', 2),
            ('pittsford', 'The Secret History', 6),
            ('pittsford', 'The Woman in White', 7),
        ])
