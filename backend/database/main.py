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

    with db.connect() as conn:
      selected_classes = conn.execute(
        "SELECT * FROM Classtime LEFT JOIN "
        "(SELECT Class.class_number AS class_num, Course.subject AS c_subject, Course.catalog_number AS c_catalog, *  "
        "FROM Class LEFT JOIN Course ON Course.subject = Class.subject AND Course.catalog_number = Class.catalog_number) "
        "AS CourseAndClass "
        "ON CourseAndClass.class_number = ClassTime.class_number "
        f"WHERE weekdays LIKE '%{weekdays}%' AND c_subject LIKE '%{subject}%' AND c_catalog LIKE '%{catalog_number}%' "
        f"AND start_time >= '{from_time}' AND end_time <= '{to_time}'"
      )
      
      # Need better way for this
      result = []
      for selected_class in selected_classes:
        class_info = {
          'start_time': selected_class['start_time'].strftime("%H:%M:%S"),
          'end_time': selected_class['end_time'].strftime("%H:%M:%S"),
          'weekdays': selected_class['weekdays'],
          'is_active': selected_class['is_active'],
          'building': selected_class['building'],
          'room': selected_class['room'],
          'subject': selected_class['subject'],
          'catalog_number': selected_class['catalog_number'],
          'units': selected_class['units'],
          'class_number': selected_class['class_num'],
          'class_type': selected_class['class_type'],
          'section_number': selected_class['section_number'],
          'description': selected_class['description'],
          'name': selected_class['name'],
        }
        result.append(class_info)
      conn.close()

      return {'classes': result }


class Courses(Resource):
  """
    '/courses' route
    GET: returns list of all the courses from SQL database (and can search)
  """
  def get(self):
    subject = request.args.get('subject') or ''
    catalog = request.args.get('catalog') or ''

    sql_command = "SELECT * FROM Course"
    if subject != '':
      sql_command += f" WHERE subject = '{subject}'"
    if catalog != '':
      sql_command += f" AND catalog_number LIKE '{catalog}%'" if subject != '' else f" WHERE catalog_number LIKE '{catalog}%'"
    with db.connect() as conn:
      all_courses = conn.execute(sql_command)
      result = [dict(row) for row in all_courses]
      print(result)
    return {'courses': result }


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


class Schedule(Resource):
  def get(self):
    username = request.args.get('username') or ''
    user_class_nums = get_users_classnums(username)
    class_schedule_list = get_class_schedule(user_class_nums)
    
    return {'schedule': class_schedule_list}

  def post(self):
    data = request.json
    class_numbers = extract_class_num(data["schedule"])
    username = data["username"]

    if username and class_numbers:
      add_user_schedule(username, class_numbers)
    
    class_schedule_list = get_class_schedule(class_numbers)

    return {'classes': class_schedule_list}


class CoursesTaken(Resource):
  def get(self):
    username = request.args.get('username')
    with db.connect() as conn:
      all_courses = conn.execute(f'SELECT * FROM CoursesTaken, Course WHERE CoursesTaken.username = \'{username}\' AND Course.subject = CoursesTaken.subject AND Course.catalog_number = CoursesTaken.catalog_number').fetchall()
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
      matched_course = conn.execute(f'SELECT * FROM Course WHERE Course.subject = \'{data["subject"]}\' AND Course.catalog_number = \'{data["catalog_number"]}\'').fetchone()
      if matched_course is None: return {'result': 'ERROR: No Such Course.'}
      matched_course = dict(matched_course.items())
      try:
        conn.execute(f'INSERT INTO CoursesTaken VALUES (\'{data["username"]}\', \'{matched_course["subject"]}\', \'{matched_course["catalog_number"]}\')')
      except:
        return {'result': 'ERROR: Course Already Exists.'}
      conn.close()
      return {'result': 'success', 'course': matched_course}
  
  def delete(self):
    username = request.args.get('username')
    subject = request.args.get('subject')
    catalog_number = request.args.get('catalog_number')
    with db.connect() as conn:
      matched_course = conn.execute(f'SELECT * FROM CoursesTaken WHERE username = \'{username}\' AND subject = \'{subject}\' AND catalog_number = \'{catalog_number}\'').fetchone()
      if matched_course is None: return {'result': 'ERROR: You have not taken this course.'}
      try:
        conn.execute(f'DELETE FROM CoursesTaken WHERE username = \'{username}\' AND subject = \'{subject}\' AND catalog_number = \'{catalog_number}\'')
      except:
        return {'result': 'ERROR: Course not uploaded.'}
      conn.close()
      return {'result': 'success'}


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
