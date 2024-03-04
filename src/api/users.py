from flask_restful import Resource
from db import example

class Users(Resource):
    def get(self):
        return example.getUsers()
