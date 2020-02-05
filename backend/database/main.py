import os
from .db_connect import db
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from webargs.flaskparser import use_args
from webargs import fields
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


class Class(Resource):
  """
    '/class?from_time=<time>&to_time=<time>&weekdays=<day>' route
    GET: returns list of classes within the specified time range and weekday
  """
  @use_args({
    "from_time": fields.Str(required=False),
    "to_time": fields.Str(required=False),
    "weekdays": fields.Str(required=False),
  })
  def get(self, args):
    from_time = args.get("from_time", '00:00:00')
    to_time = args.get("to_time", '23:59:59')
    weekdays = args.get("weekdays", '')

    with db.connect() as conn:
      selected_classes = conn.execute(
        "SELECT * FROM Classtime LEFT JOIN "
        "(SELECT Class.id AS class_id, * FROM Class LEFT JOIN Course ON Course.subject = Class.subject AND Course.catalog_number = Class.catalog_number) "
        "AS CourseAndClass "
        "ON CourseAndClass.class_id = ClassTime.class_id "
        f"WHERE weekdays LIKE '%{weekdays}%' "
        f"AND start_time >= '{from_time}' AND end_time <= '{to_time}'"
      )

      result = []
      for c in selected_classes:
        class_info = {
          'id': c['class_id'],
          'subject': c['subject'],
          'catalog_number': c['catalog_number'],
          'name': c['name'],
          'building': c['building'],
          'room': c['room'],
          'weekdays': c['weekdays'],
          'start_time': c['start_time'].strftime('%H:%M'),
          'end_time': c['end_time'].strftime('%H:%M'),
          'enrollment_capacity': c['enrollment_capacity'],
          'enrollment_total': c['enrollment_total'],
          'waiting_capacity': c['waiting_capacity'],
          'waiting_total': c['waiting_total'],
        }
        result.append(class_info)
      print(result)

      return {"classes": result}


class Courses(Resource):
  """
    '/courses' route
    GET: returns list of all the courses from SQL database (and can search)
  """
  @use_args({
    "subject": fields.Str(required=False),
    "catalog": fields.Str(required=False)
  })
  def get(self, args):
    subject = args.get("subject", '')
    catalog = args.get("catalog", '').strip()
    sql_command = "SELECT * FROM Course"
    if subject != '':
      sql_command += f" WHERE subject = '{subject}'"
    if catalog != '':
      sql_command += f" AND catalog_number LIKE '{catalog}'" if subject != '' else f" WHERE catalog_number LIKE '{catalog}%'"
    with db.connect() as conn:
      all_courses = conn.execute(sql_command)
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
api.add_resource(Class, '/class')
