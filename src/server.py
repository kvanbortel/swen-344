from flask import Flask
from flask_restful import Resource, Api
from api.books import *
from api.users import *
from api.management import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Init, '/manage/init') #Management API for initializing the DB

api.add_resource(Version, '/manage/version') #Management API for checking DB version

api.add_resource(Books, '/books')

api.add_resource(ListCheckout, '/list_checkout')

api.add_resource(Users, '/users')

api.add_resource(Login, '/login')

api.add_resource(Checkout, '/checkout')

if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True)
