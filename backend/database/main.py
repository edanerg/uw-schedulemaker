import os
from .db_connect import db
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from webargs.flaskparser import use_args
from webargs import fields
from flask_cors import CORS
from .db_functions import *

app = Flask(__name__)
api = Api(app)
CORS(app)

class Class(Resource):
  """
    '/class?from_time=<time>&to_time=<time>&weekdays=<day>&subject=<subject>&catalog_number=<num>' route
    GET: returns list of classes within the specified time range, weekday, subject and subject number
  """
  def get(self):
    from_time = request.args.get('from_time') or '00:00:00'
    to_time = request.args.get('to_time') or '23:59:59'
    weekdays = request.args.get('weekdays') or ''
    subject = request.args.get('subject') or ''
    catalog_number = request.args.get('catalog_number') or ''
    result = get_filtered_classes(from_time, to_time, weekdays, subject, catalog_number)

    return {'classes': result }


class Courses(Resource):
  """
    '/courses' route
    GET: returns list of all the courses from SQL database (and can search)
  """
  def get(self):
    subject = request.args.get('subject') or ''
    catalog = request.args.get('catalog') or ''

    result = get_courses(subject, catalog)
    return {'courses': result }


class User(Resource):
  def post(self):
    data = request.json
    result = user_profile_actions(data)
    return result


class Schedule(Resource):
  def get(self):
    username = request.args.get('username') or ''
    user_class_nums = get_users_classnums(username)
    class_schedule_list = get_class_schedule(user_class_nums)

    addable_classes_schedule = []
    if username:
      addable_classes_num = get_classes_user_can_add(username)
      addable_classes_schedule = get_class_schedule(addable_classes_num)
    return {'schedule': class_schedule_list, 'addable_classes': addable_classes_schedule}

  def post(self):
    data = request.json
    class_numbers = extract_class_num(data["schedule"])
    class_to_add = data["classToAdd"]
    class_to_remove = data["classToRemove"]
    username = data["username"]

    if username and class_numbers:
      add_user_schedule(username, class_numbers)
    elif username and class_to_add:
      add_user_schedule(username, [class_to_add])
    elif username and class_to_remove:
      remove_from_user_schedule(username, [class_to_remove])
    
    return {'result': 'success'}


class CoursesTaken(Resource):
  def get(self):
    username = request.args.get('username')
    result = get_courses_user_taken(username)
    return {'courses': result}
  
  def post(self):
    data = request.json
    result = add_user_course_taken(data)
    return result
  
  def delete(self):
    username = request.args.get('username')
    subject = request.args.get('subject')
    catalog_number = request.args.get('catalog_number')

    result = delete_course_taken(username, subject, catalog_number)
    return result

class Instructor(Resource):
  def get(self):
    instructor = request.args.get('instructor')
    result = get_instructor_classes(instructor)
    return {'classes': result}

class Main(Resource):
  """
    this is a test function
    returns msg on '/' route
  """
  def get(self):
      return "Hi there!"

api.add_resource(Main, '/')
api.add_resource(Schedule, '/schedule')
api.add_resource(Courses, '/courses')
api.add_resource(User, '/user')
api.add_resource(CoursesTaken, '/coursesTaken')
api.add_resource(Class, '/class')
api.add_resource(Instructor, '/instructor')
