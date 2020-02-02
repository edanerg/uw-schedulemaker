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
        "(SELECT Class.id AS class_id, * FROM Class LEFT JOIN Course ON Course.id = Class.course_id) "
        "AS CourseAndClass "
        "ON CourseAndClass.class_id = ClassTime.class_id "
        f"WHERE weekdays LIKE '%{weekdays}%' "
        f"AND start_time >= '{from_time}' AND end_time <= '{to_time}'"
      )

      result = []
      for c in selected_classes:
        class_info = {
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
    GET: returns list of all the courses from SQL database
    POST: todo, can grab specific course
  """
  @use_args({"subject": fields.Str(required=False), "catalog": fields.Str(required=False)})
  def get(self, args):
    subject = args.get("subject", '')
    catalog = args.get("catalog_number", '')

    with db.connect() as conn:
      all_courses = conn.execute(
        "SELECT * FROM Course "
        f"WHERE subject LIKE '{subject}' AND catalog_number LIKE '%{catalog}%'"
      )
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
api.add_resource(Class, '/class')
