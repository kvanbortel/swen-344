import unittest
from tests.test_utils import *
import json
from src.db import library
from urllib.parse import urlencode


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
        _phone = '127-654-9999'
        _email = 'yourebreathtaking@aol.com'
        _password = 'K567'

        print(f'Want to add {_name}, {_phone}, {_email}, and {_password}; we will use a POST API')
        data = dict(name=_name, phone=_phone, email=_email, password=_password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        print(f'Result [the PK of the new row]:{result}')
       
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'New contents are:\n{result}\n')

    def test_post_user_failure(self):
        """Post user fails when user already exists"""
        # Variables for the data to be sent
        _name = 'Art Garfunkel'
        _phone = '127-654-9999'
        _email = 'yourebreathtaking@aol.com'
        _password = 'K567'

        print(f'Want to add {_name}, {_phone}, {_email}, and {_password}; we will use a POST API')
        data = dict(name=_name, phone=_phone, email=_email, password=_password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr, 409)
        print(result)

    def test_param_put_user(self):
        """Edit a user's information"""
        print(f'The URL used is: http://localhost:5000 ... but there is json data in the body of the PUT')

        print('Current contents are:')
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'{result}\n')

        # Variables for the data to be sent
        _old_name = 'Art Garfunkel'
        _new_name = 'Artist Dafunkel'
        _phone = '999-999-8871'
        _email = 'thefunkel@aol.com'

        print(f'Want to modify {_old_name} user with new: {_new_name}, {_phone}, {_email}; we will use a PUT API')
        data = dict(old_name=_old_name, new_name=_new_name, phone=_phone, email=_email)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = put_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
       
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'New contents are:\n{result}\n')

    def test_put_user_failure(self):
        """Try to edit information of a user that doesn't exist"""
        # Variables for the data to be sent
        _old_name = 'DNE'
        _new_name = 'Artist Dafunkel'
        _phone = '999-999-8871'
        _email = 'thefunkel@aol.com'

        print(f'Want to modify {_old_name} user with new: {_new_name}, {_phone}, {_email}; we will use a PUT API')
        data = dict(old_name=_old_name, new_name=_new_name, phone=_phone, email=_email)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = put_rest_call(self, 'http://localhost:5000/users', jdata, hdr, 404)
        print(result)

    def test_delete_user(self):
        """Delete (deactivate) a user"""
        #Login
        _name = 'Mary Shelley'
        _password = 'password'

        data = dict(name=_name, password=_password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        session_key = json.loads(result)['session_key']

        # Delete user
        name = 'Art Garfunkel'
        print(f'User {name} was active: ' + str(library.isActive(name)))

        hdr = {'session_key': session_key}
        params = urlencode({'name': name})
        delete_rest_call(self, f'http://localhost:5000/users?{params}', hdr)

        print(f'User {name} is active: ' + str(library.isActive(name)))

    def test_delete_user_session_failure(self):
        name = 'Art Garfunkel'
        print(f'User {name} was active: ' + str(library.isActive(name)))

        hdr = {'session_key': 'NULL'}
        params = urlencode({'name': name})
        result = delete_rest_call(self, f'http://localhost:5000/users?{params}', hdr, 401)
        print(result)

        print(f'User {name} is active: ' + str(library.isActive(name)))


    def test_delete_user_DNE_failure(self):
        """Try to delete a user that doesn't exist"""
        #Login
        _name = 'Mary Shelley'
        _password = 'password'

        data = dict(name=_name, password=_password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        session_key = json.loads(result)['session_key']

        # Try to delete user that doesn't exist
        name = 'DNE'
        hdr = {'session_key': session_key}
        params = urlencode({'name': name})
        result = delete_rest_call(self, f'http://localhost:5000/users?{params}', hdr, 404)
        print(result)

    def test_get_user_checkouts(self):
        """List the books a user has checked out"""
        data = get_rest_call(self, 'http://localhost:5000/list_checkout?user=Mary%20Shelley')
        print(data)

    def test_login_failure(self):
        """Login fails with incorrect password"""
        hdr = {'content-type': 'application/json'}

        #Login
        _name = 'Mary Shelley'
        _password = 'not_password'

        data = dict(name=_name, password=_password)
        jdata = json.dumps(data)
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr, 401)
        print(result)

    def test_login_checkout_reserve_success(self):
        """Successful login returns session key"""
        hdr = {'content-type': 'application/json'}

        #Login
        _name = 'Mary Shelley'
        _password = 'password'

        data = dict(name=_name, password=_password)
        jdata = json.dumps(data)
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        print(f'\n{result}\n')
        session_key = json.loads(result)['session_key']

        # A user can check out a book if logged in
        _title = 'The Secret History'
        _library = 'test_library'
        _date = '2024-01-02'

        print('Current user checkout contents are:')
        data = get_rest_call(self, 'http://localhost:5000/list_checkout?user=Mary%20Shelley')
        print(f'{data}\n')

        data = dict(session_key=session_key)
        jdata = json.dumps(data)
        params = urlencode({'user': _name, 'title': _title, 'library': _library, 'date': _date})
        post_rest_call(self, f'http://localhost:5000/checkout?{params}', jdata, hdr)

        print('User checkout contents are now:')
        data = get_rest_call(self, 'http://localhost:5000/list_checkout?user=Mary%20Shelley')
        print(f'{data}\n')

        # Reserve a book
        _title = 'Dynasty'
        params = urlencode({'user': _name, 'title': _title, 'library': _library})
        post_rest_call(self, f'http://localhost:5000/reserve?{params}', jdata, hdr)
        self.assertEqual(library.isReserved(_title, _library), 1)

        # Logout
        data = dict(session_key=session_key, name=_name)
        jdata = json.dumps(data)
        put_rest_call(self, 'http://localhost:5000/logout', jdata, hdr)

    def test_checkout_reserve_session_failure(self):
        hdr = {'content-type': 'application/json'}
        # A user can't check out a book if not logged in
        _name = 'Mary Shelley'
        _title = 'The Secret History'
        _library = 'test_library'
        _date = '2024-01-02'

        data = dict(session_key='NULL')
        jdata = json.dumps(data)
        params = urlencode({'user': _name, 'title': _title, 'library': _library, 'date': _date})
        result = post_rest_call(self, f'http://localhost:5000/checkout?{params}', jdata, hdr, 401)
        print(result)

        # A user can't reserve a book if not logged in
        _title = 'Dynasty'
        params = urlencode({'user': _name, 'title': _title, 'library': _library})
        post_rest_call(self, f'http://localhost:5000/reserve?{params}', jdata, hdr, 401)
        print(result)
        self.assertEqual(library.isReserved(_title, _library), 0)
