from flask_restful import Resource, reqparse, request
from db import library
from db.swen344_db_utils import *
import json
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
        user_id, = exec_get_one("""
            SELECT users.id FROM users
            WHERE users.name = %s
        """, (old_name,))
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
        name = request.args['name']
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
        try:
            user_id, = exec_get_one("""
                SELECT users.id FROM users
                WHERE users.name = %s and users.password = %s
            """, (name, pwd_digest))
        except TypeError:
            return 'Login unsuccessful. User not found', 404
        # Generate session key
        session_key = secrets.token_bytes(16)
        # Add session key
        exec_commit("""
            UPDATE users SET session_key = %s
            WHERE id = %s
        """, (session_key, user_id))
        data = dict(
            message=f'Login successful.',
            session_key=base64.b64encode(session_key).decode(),
        )
        return json.dumps(data)

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
            return 'User not authenticated', 401
        user = request.args['user']
        title = request.args['title']
        _library = request.args['library']
        date = request.args['date']
        library.checkoutBook(user, title, _library, date)

class Reserve(Resource):
    def post(self):
        """A user reserves a book"""
        if not library.isAuthenticated():
            return 'User not authenticated', 401
        user = request.args['user']
        title = request.args['title']
        _library = request.args['library']
        library.reserveBook(user, title, _library)
