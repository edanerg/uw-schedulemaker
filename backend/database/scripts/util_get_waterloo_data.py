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


def get_class_schedule(class_number):
  r = requests.get(
      f'https://api.uwaterloo.ca/v2/courses/{class_number}/schedule.json', params=params)
  class_schedule = r.json()['data'][0]

  return class_schedule


def get_all_courses():
  r = requests.get(
    'https://api.uwaterloo.ca/v2/codes/subjects.json', params=params)
  all_subjects = r.json()['data']
  # all_subjects = [{"subject": "STAT", "description": "Statistics",
  #                  "unit": "STATACTSC", "group": "MAT"}]

  # grabs 10 courses for each subject
  all_courses = []
  for subject_info in all_subjects:
    subject = subject_info['subject']
    r = requests.get(
        f'https://api.uwaterloo.ca/v2/courses/{subject}.json', params=params)
    courses = r.json()['data']
    courses = courses[:10]

    # get more info about specific course
    for course_info in courses:
      catalog_number = course_info['catalog_number']
      r = requests.get(
          f'https://api.uwaterloo.ca/v2/courses/{subject}/{catalog_number}.json', params=params)
      more_info = r.json()['data']
      course_info['prerequisites'] = more_info.get('prerequisites','')
      course_info['antirequisites'] = more_info.get('antirequisites', '')
      all_courses.append(course_info)

  return all_courses
