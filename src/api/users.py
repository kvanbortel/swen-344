from flask_restful import Resource
from db import library

class Users(Resource):
    def get(self):
        return library.getUsers()
