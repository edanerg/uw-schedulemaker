import sqlalchemy
import re
import argparse
from sys import argv
from util_get_waterloo_data import get_all_courses, get_course, get_course_schedule

def populate_courses(db): 
  """
    Populates Courses tables
    Grabs all courses at /courses
    Grabs Course description at /course/{course_id}
  """
  courses = get_all_courses()
  with db.connect() as conn:
    for course in courses:
      course_id = course['course_id']
      subject = course['subject']
      catalog_number = course['catalog_number']
      name = course['title'].replace('\'', '\'\'')
      print(f"Adding {subject} {catalog_number} into Course table")

      # grabs info for specific course
      course_info = get_course(course_id)
      course_description = course_info['description']
      if course_description:
        course_description = course_description.replace('\'', '\'\'')
      else:
        course_description = "NULL"

      command = f"INSERT INTO Course VALUES ('{course_id}', '{subject}', '{catalog_number}', " \
          f"'{name}', '{course_description}') "
      conn.execute(command)

    print("All Courses are now added")


def populate_classes_classtime(db):
  """
    Populates Classes and Classtime tables
    Grabs the schedules for each course at /courses/{subject}/{catalog_number}
  """
  # Get all existing courses in the Course table
  with db.connect() as conn:
    all_courses_from_table = conn.execute("SELECT * FROM Course")
    courses = [{
        'subject': dict(row)['subject'],
        'catalog_number': dict(row)['catalog_number']
    } for row in all_courses_from_table]

  print("Grabing schedule for each course from waterloo api, will take a longggg time")
  courses_schedule = []
  for course in courses:
    schedule = get_course_schedule(course['subject'], course['catalog_number'])
    if schedule:
      courses_schedule += schedule
  
  print("Sucessfully obtained all data, now populating tables")
  with db.connect() as conn:
    # Not sure if have to check if values in the api data is null
    for schedule in courses_schedule:
      print(f"Adding {schedule} to Class table")
      subject = schedule['subject']
      catalog_number = schedule['catalog_number']
      units = schedule['units']
      note = schedule['note'] or ''
      class_number = schedule['class_number']
      
      section = schedule['section'].split()
      class_type = section[0]
      section_number = section[1]

      campus = schedule['campus']
      associated_class = schedule['associated_class']
      related_component_1 = schedule['related_component_1'] or '0'
      related_component_2 = schedule['related_component_2'] or '0'
      enrollment_capacity = schedule['enrollment_capacity']
      enrollment_total = schedule['enrollment_total']
      waiting_capacity = schedule['waiting_capacity']
      waiting_total = schedule['waiting_total']
      topic = schedule['topic'] or ''
      held_with = ','.join(schedule['held_with'])
      term = schedule['term']
      academic_level = schedule['academic_level']
      class_id = f'{subject}-{catalog_number}-{class_type}-{section_number}'

      command = (
        "INSERT INTO Class VALUES ( "
        f"'{class_id}', '{subject}', '{catalog_number}', "
        f"'{units}', '{note}', '{class_number}', "
        f"'{class_type}', '{section_number}', '{campus}', "
        f"'{associated_class}', '{related_component_1}', '{related_component_2}', "
        f"'{enrollment_capacity}', '{enrollment_total}', '{waiting_capacity}', "
        f"'{waiting_total}', '{topic}', '{held_with}', "
        f"'{term}', '{academic_level}' ) "
      )
      conn.execute(command)

      class_times = schedule['classes']
      last_updated = schedule['last_updated']
      current_year = last_updated.split('-')[0]

      # Populates Classtime table
      for class_time in class_times:
        date = class_time['date']
        building = class_time['location']['building']
        room = class_time['location']['room']
        start_time = date['start_time']
        end_time = date['end_time']
        weekdays = date['weekdays']

        # Not sure how to add null to datetime
        default_date = '1900-01-01'
        start_date = date['start_date'] or default_date
        end_date = date['end_date'] or default_date
        if start_date != default_date:
          start_date = f"{current_year}-{start_date.replace('/', '-')}"
        if end_date != default_date:
          end_date = f"{current_year}-{end_date.replace('/', '-')}"
        
        is_active = not (date['is_tba'] and date['is_cancelled'] and date['is_closed'])
        # can change this id
        classtime_id = f'{building}-{room}-{start_date}-{start_time}-{weekdays}'
        command = (
          "INSERT INTO ClassTime VALUES ( "
          f"'{classtime_id}', '{class_id}', '{start_time}', "
          f"'{end_time}', '{weekdays}', '{start_date}', "
          f"'{end_date}', '{is_active}', '{building}', "
          f"'{room}'); "
        )
        conn.execute(command)

  print("Sucessfully added all data")



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", dest="table", required=True)
  parser.add_argument("-u", dest="user", required=False, default="root")
  parser.add_argument("-p", dest="password", required=False, default="tmp")

  arguments = parser.parse_args()

  db = sqlalchemy.create_engine(
    f'postgresql+pg8000://{arguments.user}:{arguments.password}@localhost:5432/schedulemaker')

  table = arguments.table

  if table == "Course":
    populate_courses(db)
  elif table == "Class":
    print("Will populate Class table according to the courses in Course table")
    populate_classes_classtime(db)
  elif table == "ClassTime":
    print("Classtime table will be populated when Class table gets populated")
  else:
    populate_courses(db)
    populate_classes_classtime(db)
    print("If error occurs, there are probably values in the table already" \
          ", execute purgetables and try again")



