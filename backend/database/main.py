from flask import Flask
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

# TODO: Change to receive data from database
class Courses(Resource):
    def get(self):
        return {'courses': ['cs', 'maths', 'biology']}


class Main(Resource):
    def get(self):
        return "Hi there!"


# TODO: add more routes
api.add_resource(Main, '/')
api.add_resource(Courses, '/courses')

