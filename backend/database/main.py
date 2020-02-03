import os
from .db_connect import db
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

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


class User(Resource):
  def post(self):
    data = request.json
    if data['action'] == 'login':
      with db.connect() as conn:
        user = conn.execute(f'SELECT * FROM AppUser WHERE username = \'{data["username"]}\'').fetchone()
        conn.close()
        return {'user': dict(user.items()) if user else None}

    elif data['action'] == 'signup':
      with db.connect() as conn:
        conn.execute(f'INSERT INTO AppUser (username) VALUES (\'{data["username"]}\')')
        conn.close()
        return {'result': 'success'}
    
    elif data['action'] == 'uploadSchedule':
      with db.connect() as conn:
        conn.execute(f'UPDATE AppUser SET schedule = \'{data["schedule"]}\' WHERE username = \'{data["username"]}\'')
        conn.close()
        return {'result': 'success'}


class CoursesTaken(Resource):
  def get(self):
    username = request.args.get('username')
    with db.connect() as conn:
      all_courses = conn.execute(f'SELECT * FROM CoursesTaken, Course WHERE CoursesTaken.username = \'{username}\' AND Course.id = CoursesTaken.course_id').fetchall()
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
      conn.close()
      return {'courses': result}
  
  def post(self):
    data = request.json
    with db.connect() as conn:
      conn.execute(f'INSERT INTO CoursesTaken VALUES (\'{data["username"]}\', {data["courseId"]})')
      conn.close()
      return {'result': 'success'}
  
  def delete(self):
    data = request.json
    with db.connect() as conn:
      conn.execute(f'DELETE FROM CoursesTaken WHERE username = \'{data["username"]}\' AND course_id = {data["courseId"]}')
      conn.close()
      return {'result': 'success'}


# TODO: add more routes
api.add_resource(Main, '/')
api.add_resource(Courses, '/courses')
api.add_resource(User, '/user')
api.add_resource(CoursesTaken, '/coursesTaken')
