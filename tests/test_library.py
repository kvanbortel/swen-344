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
        """Verify seeded table returns correct books list for user"""
        exec_sql_file("db-kjv7359/src/library.sql")
        books = listUserBooks("Jackie Gleason") # Do Art Garfunkel
        self.assertEqual(books, ['The Woman in White'])
