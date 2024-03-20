from flask_restful import Resource, reqparse, request
from db import library
from db.swen344_db_utils import *
import secrets
import base64

class Users(Resource):
    def get(self):
        return library.getUsers()

    def post(self):
        """Extracts data from body and adds a row"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        name = args.name
        phone = args.phone
        email = args.email
        password = args.password
        pwd_digest = library.hashPassword(password)
        # Check if user already exists
        exists, = exec_get_one("""
            SELECT EXISTS
                (SELECT users.id FROM users
                WHERE users.name = %s)
        """, (name,))
        if exists:
            return library.makeError('User already exists', 409)
        # Add new row to users table
        result = exec_commit_with_id("""
            INSERT INTO users (name, phone, email, password)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, phone, email, pwd_digest))
        return result

    def put(self):
        """Extracts data from body and updates user row"""
        parser = reqparse.RequestParser()
        parser.add_argument('old_name', type=str)
        parser.add_argument('new_name', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        old_name = args.old_name
        new_name = args.new_name
        phone = args.phone
        email = args.email
        # Find the users row that relates to the given user
        result = exec_get_one("""
            SELECT users.id FROM users
            WHERE users.name = %s
        """, (old_name,))
        if result is None:
                return library.makeError('User doesn\'t exist', 404)
        user_id = result,
        # Now change the data for that user
        result = exec_commit_with_id("""
            UPDATE users SET name = %s, phone = %s, email = %s
            WHERE id = %s
            RETURNING id
        """, (new_name, phone, email, user_id))
        print(f'PUT: returning {result}')
        return result

    def delete(self):
        """Deactivates a user"""
        # Check if user is authenticated
        if not library.isAuthenticated():
            return library.makeError('User not authenticated', 401)
        # Check if user exists
        name = request.args['name']
        exists, = exec_get_one("""
            SELECT EXISTS
                (SELECT users.id FROM users
                WHERE users.name = %s)
        """, (name,))
        print(exists)
        if not exists:
            return library.makeError('User doesn\'t exist', 404)
        # Deactivate user
        exec_commit("""
            UPDATE users SET active = FALSE
            WHERE users.name = %s
        """, (name,))

class Login(Resource):
    def post(self):
        """Gives user a session key"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        name = args.name
        password = args.password
        pwd_digest = library.hashPassword(password)
        # Check if name/pwd exists in users
        result = exec_get_one("""
            SELECT users.id FROM users
            WHERE users.name = %s and users.password = %s
        """, (name, pwd_digest))
        if result is None:
            return library.makeError('Incorrect username or password', 401)
        user_id = result,
        # Generate session key
        session_key = secrets.token_bytes(16)
        # Add session key
        exec_commit("""
            UPDATE users SET session_key = %s
            WHERE id = %s
        """, (session_key, user_id))
        return dict(
            message='Login successful.',
            session_key=base64.b64encode(session_key).decode(),
        )

class Logout(Resource):
    def put(self):
        """A user logs out"""
        if not library.isAuthenticated():
            return 'User not authenticated', 401
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        name = args.name
        exec_commit("""
            UPDATE users SET session_key = NULL
            WHERE users.name = %s
        """, (name,))

class Checkout(Resource):
    def post(self):
        """A user checks out a book"""
        if not library.isAuthenticated():
            return library.makeError('User not authenticated', 401)
        user = request.args['user']
        title = request.args['title']
        _library = request.args['library']
        date = request.args['date']
        library.checkoutBook(user, title, _library, date)

class Reserve(Resource):
    def post(self):
        """A user reserves a book"""
        if not library.isAuthenticated():
            return library.makeError('User not authenticated', 401)
        user = request.args['user']
        title = request.args['title']
        _library = request.args['library']
        library.reserveBook(user, title, _library)
