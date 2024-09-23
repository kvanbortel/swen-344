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


    def login(self, name, password, code=200):
        """
        A user logs in
    
        Args:
            name:       the user's name
            password:   the user's password
            code:       the expected error code
    
        Returns:
            json success message ('message') and session key ('session_key')
            json message and code if error
        """
        data = dict(name=name, password=password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr, code)
        print(f'Login result: {result["message"]}')
        if code == 200:
            print(f'Session key: {result["session_key"]}')
        return result

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
        print('List all nonfiction books')
        result = get_rest_call(self, 'http://localhost:5000/books?type=nonfiction')
        self.assertEqual(15, len(result))

    def test_book_author_param(self):
        """Return books with author parameter"""
        result = get_rest_call(self, 'http://localhost:5000/books?author=Terry%20Pratchett')
        self.assertEqual(5, len(result))

    def test_book_library_title_params(self):
        """Return books with library and title parameters"""
        print('List all books with title \'Dynasty\'')
        result = get_rest_call(self, 'http://localhost:5000/books?location=pittsford&title=Dynasty')
        self.assertEqual(1, len(result))

    def test_book_title_not_found(self):
        """Return an empty list if title doesn't exist"""
        result = get_rest_call(self, 'http://localhost:5000/books?title=DNE')
        self.assertEqual(0, len(result))

    def test_post_user(self):
        """Add a new user to the database"""
        print('Add a new user to the database')
        # Variables for the data to be sent
        name = 'Keanu Reeves'
        phone = '127-654-9999'
        email = 'yourebreathtaking@aol.com'
        password = 'K567'

        # Add the user
        print(f'Want to add {name}, {phone}, {email}, and {password}')
        data = dict(name=name, phone=phone, email=email, password=password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        print(f'Result [the PK of the new row]:{result}')
       
        # Result
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'New user table contents are:\n{result}\n')
        self.assertEqual(5, len(result))

    def test_post_user_failure(self):
        """Post user fails when user already exists"""
        print('A user cannot be added if their name is already in the database')
        # Variables for the data to be sent
        name = 'Art Garfunkel'
        phone = '127-654-9999'
        email = 'yourebreathtaking@aol.com'
        password = 'K567'

        # Try and fail to add the user
        print(f'Want to add {name}, {phone}, {email}, and {password}')
        data = dict(name=name, phone=phone, email=email, password=password)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}

        # Result
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr, 409)
        print(f'Error: {result["message"]}')

    def test_put_user(self):
        """Edit a user's information"""
        print('Edit a user\'s information')

        # Before editing info
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'Current user table contents are:\n{result}\n')

        # Variables for the data to be sent
        old_name = 'Art Garfunkel'
        new_name = 'Artist Dafunkel'
        phone = '999-999-8871'
        email = 'thefunkel@aol.com'

        # Edit user info
        print(f'Want to modify {old_name} user with new: {new_name}, {phone}, {email}')
        data = dict(old_name=old_name, new_name=new_name, phone=phone, email=email)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = put_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
       
        # Result
        result = get_rest_call(self, 'http://localhost:5000/users')
        print(f'New user table contents are:\n{result}\n')
        for key, name, _phone, _email in result:
            self.assertNotEqual(name, old_name)
            if name == new_name:
                break
        else:
            raise AssertionError('User not found')
        self.assertEqual(_phone, phone)
        self.assertEqual(_email, email)

    def test_put_user_failure(self):
        """Try to edit information of a user that doesn't exist"""
        print('Try to edit information of a user that doesn\'t exist')
        # Variables for the data to be sent
        old_name = 'DNE'
        new_name = 'Artist Dafunkel'
        phone = '999-999-8871'
        email = 'thefunkel@aol.com'

        # Try to edit info of a user that doesn't exist
        print(f'Want to modify {old_name} user with new: {new_name}, {phone}, {email}')
        data = dict(old_name=old_name, new_name=new_name, phone=phone, email=email)
        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = put_rest_call(self, 'http://localhost:5000/users', jdata, hdr, 404)
        print(f'Error: {result["message"]}')

    def test_delete_user(self):
        """Delete (deactivate) a user"""
        print('Remove (deactivate) a user')
        #Login
        name = 'Mary Shelley'
        password = 'password'

        result = self.login(name, password)
        session_key = result['session_key']

        # Delete user while logged in
        name = 'Art Garfunkel'
        print(f'User {name} was active: ' + str(library.isActive(name)))

        hdr = {'session_key': session_key}
        params = urlencode({'name': name})
        delete_rest_call(self, f'http://localhost:5000/users?{params}', hdr)

        # Result
        print(f'User {name} is active: ' + str(library.isActive(name)))
        self.assertFalse(library.isActive(name))

    def test_delete_user_session_failure(self):
        """Cannot delete user if not logged in"""
        print('Try to delete a user without logging in')
        name = 'Art Garfunkel'
        print(f'User {name} was active: ' + str(library.isActive(name)))

        # Try to delete user
        hdr = {'session_key': 'NULL'}
        params = urlencode({'name': name})
        result = delete_rest_call(self, f'http://localhost:5000/users?{params}', hdr, 401)
        print(f'Error: {result["message"]}')

        # Result
        print(f'User {name} is active: ' + str(library.isActive(name)))
        self.assertTrue(library.isActive(name))

    def test_delete_user_DNE_failure(self):
        """Try to delete a user that doesn't exist"""
        print('Try to remove (deactivate) a user that doesn\'t exist')
        #Login
        name = 'Mary Shelley'
        password = 'password'

        result = self.login(name, password)
        session_key = result['session_key']

        # Try to delete user that doesn't exist
        name = 'DNE'
        hdr = {'session_key': session_key}
        params = urlencode({'name': name})
        result = delete_rest_call(self, f'http://localhost:5000/users?{params}', hdr, 404) 
        print(f'Error: {result["message"]}')

    def test_get_user_checkouts(self):
        """List the books a user has checked out"""
        name = 'Mary Shelley'
        params = urlencode({'user': name})
        data = get_rest_call(self, f'http://localhost:5000/list_checkout?{params}')
        print(data)
        self.assertEqual(5, len(data))

    def test_login_failure(self):
        """Login fails with incorrect password"""
        name = 'Mary Shelley'
        password = 'not_password'
        result = self.login(name, password, 401)
        print(f'Error: {result["message"]}')

    def test_login_checkout_reserve_success(self):
        """Successful login returns session key and user can checkout and reserve"""
        print('Logged in user can checkout and reserve')
        #Login
        name = 'Mary Shelley'
        password = 'password'

        result = self.login(name, password)
        session_key = result['session_key']

        # A user can check out a book if logged in
        title = 'The Secret History'
        _library = 'test_library'
        date = '2024-01-02'

        params = urlencode({'user': name})
        data = get_rest_call(self, f'http://localhost:5000/list_checkout?{params}')
        print(f'Current user checkout contents are:\n{data}\n')

        hdr = {'session_key': session_key}
        params = urlencode({'user': name, 'title': title, 'library': _library, 'date': date})
        post_rest_call(self, f'http://localhost:5000/checkout?{params}', post_header=hdr)

        params = urlencode({'user': name})
        data = get_rest_call(self, f'http://localhost:5000/list_checkout?{params}')
        print(f'User checkout contents are now:\n{data}\n')
        self.assertEqual(6, len(data))

        # A user can reserve a book if logged in
        title = 'Dynasty'
        params = urlencode({'user': name, 'title': title, 'library': _library})
        post_rest_call(self, f'http://localhost:5000/reserve?{params}', post_header=hdr)
        isReserved = library.isReserved(title, _library)
        print(f'Book is now reserved: {isReserved}')
        self.assertTrue(isReserved)

        # A user can logout if logged in
        hdr = {'content-type': 'application/json', 'session_key': session_key}
        data = dict(name=name)
        jdata = json.dumps(data)
        put_rest_call(self, 'http://localhost:5000/logout', jdata, hdr)
        print('Logged out okay')

    def test_checkout_reserve_session_failure(self):
        """A user cannot checkout or reserve a book if not logged in"""
        print('A user cannot checkout or reserve a book if not logged in')
        # A user can't check out a book if not logged in
        name = 'Mary Shelley'
        title = 'The Secret History'
        _library = 'test_library'
        date = '2024-01-02'

        params = urlencode({'user': name, 'title': title, 'library': _library, 'date': date})
        hdr = {'session_key': 'NULL'}
        result = post_rest_call(self, f'http://localhost:5000/checkout?{params}', post_header=hdr, expected_code=401)
        print(f'Error: {result["message"]}')

        # A user can't reserve a book if not logged in
        title = 'Dynasty'
        params = urlencode({'user': name, 'title': title, 'library': _library})
        post_rest_call(self, f'http://localhost:5000/reserve?{params}', post_header=hdr, expected_code=401)
        print(f'Error: {result["message"]}')
        self.assertEqual(library.isReserved(title, _library), 0)
