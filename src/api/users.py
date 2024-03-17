from flask_restful import Resource, reqparse, request
from db import library
from db.swen344_db_utils import *
import json

class Users(Resource):
    def get(self):
        return library.getUsers()

    def post(self):
        """Extracts data from body and adds a row"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        name = args['name']
        phone = args['phone']
        email = args['email']
        # Add new row to users table
        result = exec_commit_with_id("""
            INSERT INTO users (name, phone, email)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, phone, email))
        return result

    def put(self):
        """Extracts data from body and updates user row"""
        parser = reqparse.RequestParser()
        parser.add_argument('old_name', type=str)
        parser.add_argument('new_name', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        old_name = args['old_name']
        new_name = args['new_name']
        phone = args['phone']
        email = args['email']
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
        print('PUT: returning ' + str(result))
        return result

    def delete(self):
        """Deactivates a user"""
        name = request.args['name']
        exec_commit("""
            UPDATE users SET active = FALSE
            WHERE users.name = %s
        """, (name,))
