import unittest
from tests.test_utils import *


class TestExample(unittest.TestCase):

    def setUp(self):  
        """Initialize DB using API call"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        print("DB Should be reset now")

    def test_hello_world(self):
        expected = { '1' : 'hello, world!' }
        actual = get_rest_call(self, 'http://localhost:5000')
        self.assertEqual(expected, actual)

    def test_get_users(self):
        """Ensure all users are listed"""
        result = get_rest_call(self, 'http://localhost:5000/users')
        self.assertEqual(4, len(result))

    def test_get_books(self):
        """Ensure all books are listed"""
        result = get_rest_call(self, 'http://localhost:5000/books')
        self.assertEqual(35, len(result))

    def test_book_type_param(self):
        """Return books with type parameter"""
        result = get_rest_call(self, 'http://localhost:5000/books?type=nonfiction')
        self.assertEqual(15, len(result))

    def test_book_author_param(self):
        """Return books with author parameter"""
        result = get_rest_call(self, 'http://localhost:5000/books?author=Terry%20Pratchett')
        self.assertEqual(5, len(result))

    def test_book_library_title_params(self):
        """Return books with library and title parameters"""
        result = get_rest_call(self, 'http://localhost:5000/books?location=pittsford&title=Dynasty')
        self.assertEqual(1, len(result))
