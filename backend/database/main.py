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

@app.before_first_request
def create_tables():
  """
    this is a test function
    will execute when frontend does it's first api request
    executes sql commands from create tables file
  """
  with db.connect() as conn:
      for command in createtable_file_commands:
          if command:
            conn.execute(command)


class Courses(Resource):
  """
    '/courses' route
    GET: returns list of all the courses from SQL database
    POST: todo, can grab specific course
  """
  def get(self):
    with db.connect() as conn:
      all_courses = conn.execute("SELECT * FROM Course")
      result = []
      for course in all_courses:
        course_info = {
          'id': course['id'],
          'subject': course['subject'],
          'catalog_number': course['catalog_number'],
          'name': course['name'],
          'description': course['description'],
        }
        result.append(course_info)
      return {'courses': result}


class Main(Resource):
  """
    this is a test function
    returns msg on '/' route
  """
  def get(self):
      return "Hi there!"

# TODO: add more routes
api.add_resource(Main, '/')
api.add_resource(Courses, '/courses')
