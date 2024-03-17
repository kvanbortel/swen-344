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
        return result;
