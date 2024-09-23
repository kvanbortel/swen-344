import unittest
from tests.test_utils import *

class TestDBSchema(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        b_count = get_rest_call(self, 'http://localhost:5000/books')
        u_count = get_rest_call(self, 'http://localhost:5000/users')
        self.assertEqual(len(b_count), 35)
        self.assertEqual(len(u_count), 4)

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        post_rest_call(self, 'http://localhost:5000/manage/init')
        b_count = get_rest_call(self, 'http://localhost:5000/books')
        u_count = get_rest_call(self, 'http://localhost:5000/users')
        self.assertEqual(len(b_count), 35)
        self.assertEqual(len(u_count), 4)
