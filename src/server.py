from flask import Flask
from flask_restful import Resource, Api
from api.hello_world import HelloWorld
from api.management import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Init, '/manage/init') #Management API for initializing the DB

api.add_resource(Version, '/manage/version') #Management API for checking DB version

api.add_resource(HelloWorld, '/') 


if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True)
