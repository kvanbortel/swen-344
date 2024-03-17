import unittest
from tests.test_utils import *
import json


class TestLibrary(unittest.TestCase):

    def setUp(self):  
        """Initialize DB using API call"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        print("DB Should be reset now")

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

    def test_book_title_not_found(self):
        """Return an empty list if title doesn't exist"""
        result = get_rest_call(self, 'http://localhost:5000/books?title=DNE')
        self.assertEqual(0, len(result))

    def test_param_post_user(self):
        """Add a new user to the database"""
        print(f'The URL used is: http://localhost:5000 ... but there is json data in the body of the POST')

        print('Current contents are:')
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'{result}\n')

        # Variables for the data to be sent
        _name = 'Keanu Reeves'
        _phone = '127-6543-999'
        _email = 'yourebreathtaking@aol.com'

        print(f'Want to add {_name}, {_phone}, and {_email}; we will use a POST API')
        data = dict(name=_name, phone=_phone, email=_email)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        print(f'Result [the PK of the new row]:{result}')
       
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'New contents are:\n{result}\n')
