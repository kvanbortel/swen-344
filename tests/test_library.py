import unittest
from src.library import *
from src.swen344_db_utils import connect

class TestLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize and seed the database"""
        exec_sql_file("db-kjv7359/src/init_db.sql")
        exec_sql_file("db-kjv7359/tests/seed_test_db.sql")

    def test_verify_rows(self):
        """Check the number of rows for each table"""
        self.assertEqual(countRows("users"), 4)
        self.assertEqual(countRows("books"), 6)
        self.assertEqual(countRows("book_status"), 10)
        self.assertEqual(countRows("book_availability"), 6)

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
            ('Dynasty', 7),
            ('The Making of a Story', 5),
            ('The Midnight Disease', 10),
        ])

    def test_list_books_date(self):
        """Check the output of listBooksByDate()"""
        title_date_tuples = listBooksByDate()
        self.assertEqual(title_date_tuples, [
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
            'book_availability',
            'book_status',
            'books',
            'users'
        ])

    def test_book_type_totals(self):
        """Ensure countType() returns correct types and counts"""
        type_count_tuples = countType()
        self.assertEqual(type_count_tuples,
            [('fiction', 3), ('nonfiction', 3)]
        )
