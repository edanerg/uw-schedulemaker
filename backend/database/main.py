import os
from .db_connect import db
from flask import Flask
from flask_restful import Resource, Api
from json import dumps
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

sql_folder = f'{os.getcwd()}/database/sql/'

# Open and read the createtables.sql and sampledataset file
path_to_createtables = f'{sql_folder}createtables.sql'
fd = open(path_to_createtables, 'r')
createtable_file = fd.read()
fd.close()
# Get the createtables commands
createtable_file_commands = createtable_file.split(';')


# create_tables() will execute when frontend does it's first api request
# can add an admin button to do this
@app.before_first_request
def create_tables():
  with db.connect() as conn:
      # Execute every command from the createtables file
      for command in createtable_file_commands:
          if command:
            conn.execute(command)


class Courses(Resource):
  def get(self):
      return {'courses': ['cs', 'maths', 'biology']}


class Main(Resource):
  def get(self):
      return "Hi there!"

# TODO: add more routes
api.add_resource(Main, '/')
api.add_resource(Courses, '/courses')
