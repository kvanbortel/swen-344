import unittest
from src.library import *
from src.swen344_db_utils import connect

class TestLibrary(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        rebuildTables()
        result = exec_get_all('SELECT * FROM example_table')
        self.assertEqual([], result, "no rows in example_table")

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuildTables()
        rebuildTables()
        result = exec_get_all('SELECT * FROM example_table')
        self.assertEqual([], result, "no rows in example_table")

    def test_verify_rows(self):
        """Verify seeded tales have correct num rows"""
        exec_sql_file("db-kjv7359/src/library.sql")
        self.assertEqual(countRows("users"), 4)
        self.assertEqual(countRows("books"), 6)
        self.assertEqual(countRows("status"), 6)

    def test_list_user_books_empty(self):
        """Verify seeded table returns empy list for user with no items"""
        exec_sql_file("db-kjv7359/src/library.sql")
        books = listUserBooks("Art Garfunkel")
        self.assertEqual(books, [])

    def test_list_user_books_alphabetical(self):
        """Verify seeded table returns correct books list for user"""
        exec_sql_file("db-kjv7359/src/library.sql")
        books = listUserBooks("Jackie Gleason")
        self.assertEqual(books, ['Dynasty', 'Mort', 'The Woman in White'])

    def test_list_all_checked_out_books(self):
        """Verify seeded table returns all checked out titles by user name"""
        exec_sql_file("db-kjv7359/src/library.sql")
        name_book_tuples = listAllCheckedOutBooks()
        self.assertEqual(name_book_tuples,
            [('Ada Lovelace',   'Dynasty',),
             ('Ada Lovelace',   'The Secret History',),
             ('Jackie Gleason', 'Dynasty',),
             ('Jackie Gleason', 'Mort',),
             ('Jackie Gleason', 'The Woman in White',),
             ('Mary Shelley',   'Dynasty',),
             ('Mary Shelley',   'Mort',),
             ('Mary Shelley',   'The Making of a Story',),
             ('Mary Shelley',   'The Midnight Disease',),
             ('Mary Shelley',   'The Woman in White',)]
        )

    def test_list_nonfiction_quantity_books(self):
        """Verify seeded table returns all nonfiction titles and quantity"""
        exec_sql_file("db-kjv7359/src/library.sql")
        title_quantity_tuples = listTypeBooks("nonfiction")
        self.assertEqual(title_quantity_tuples,
            [('Dynasty', 7,),
             ('The Making of a Story', 5,),
             ('The Midnight Disease', 10,)]
        )
