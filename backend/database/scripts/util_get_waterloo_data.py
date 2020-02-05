import requests

params = {'key': '6642768b60d4b5dcde0d2d10db5500fa'}


def get_course(course_id):
  r = requests.get(
    f'https://api.uwaterloo.ca/v2/courses/{course_id}.json', params=params)
  course = r.json()['data']

  return course

def get_course_schedule(subject, catalog_number):
  r = requests.get(
    f'https://api.uwaterloo.ca/v2/courses/{subject}/{catalog_number}/schedule.json', params=params)
  course_schedule = r.json()['data']

  return course_schedule

def get_all_courses():
  r = requests.get(
    'https://api.uwaterloo.ca/v2/courses.json', params=params)
  courses = r.json()['data']

  return courses

