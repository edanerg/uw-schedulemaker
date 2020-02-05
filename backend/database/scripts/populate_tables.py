import sqlalchemy
import re
import argparse
from sys import argv
from util_get_waterloo_data import get_all_courses, get_course

def populate_courses(courses, db): 
  """
    Populates Courses tables
    Grabs all courses at /courses
    Grabs Course description at /course/{course_id}
  """
  with db.connect() as conn:
    for course in courses:
      course_id = course['course_id']
      subject = course['subject']
      catalog_number = course['catalog_number']
      name = course['title'].replace('\'', '\'\'')

      course_info = get_course(course_id)
      course_description = course_info['description']
      if course_description:
        course_description = course_description.replace('\'', '\'\'')
      else:
        course_description = "NULL"

      command = f"INSERT INTO Course VALUES ('{course_id}', '{subject}', '{catalog_number}', " \
          f"'{name}', '{course_description}') "
      conn.execute(command)



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", dest="table", required=True)
  parser.add_argument("-u", dest="user", required=False, default="root")
  parser.add_argument("-p", dest="password", required=False, default="tmp")

  arguments = parser.parse_args()

  db = sqlalchemy.create_engine(
    f'postgresql+pg8000://{arguments.user}:{arguments.password}@localhost:5432/schedulemaker')

  if arguments.table == "course":
    courses = get_all_courses()
    populate_courses(courses, db)
