import sqlalchemy
import re
import argparse
from sys import argv
from util_get_waterloo_data import *
from sqlalchemy import text

def make_string_sql_safe(s, default_char):
  if s:
    return s.replace('\'', '\'\'')
  return default_char


def process_primary_component(conn, primary, related_components, component_type):
  """
    Determines the class number of the related components. component_type is either related_component_1 
    or related_component_2.
    Suppose the primary component is lectures, related component is tutorials, and component type is 1.
    - If there are no tutorials, then set the lecture's related_component_1 to 0 (this is already done by default).
    - If the lecture's related_component_1 is not null, then set the lecture's related_component_1
      to the class_number of the tutorial with a section_number equal to lecture's related_component_1
    - If the lecture's related_component_1 is null, then there must be some matching tutorials. Iterate through the tutorials.
      - If there is exactly two or more tutorials with a matching associated_class, then set the
        lecture's related_component_1 to 1. Also set the tutorials' related_component_1 to the lecture's
        class_number
      - Otherwise, the lecture can be taken with any tutorial, so set the lecture's related_component_1
        to 2.
    - Online classes have related components if and only if its related_component_1 is not null or it has a
      matching associated class number with a related component.
    The results of this will be used in db_functions/get_classes_user_can_add to ensure that a primary
    component is included if and only if its second and third components are included
  """
  class_number = primary['class_number']
  print(f"Class number {class_number}")
  if primary[component_type]:
    allowed_first_comps = list(filter(lambda comp:
      comp['section'].split()[1] == primary[component_type], related_components
    ))
    if allowed_first_comps:
      comp_class_number = allowed_first_comps[0]['class_number']
      # Update primary component
      conn.execute(f"UPDATE Class SET {component_type} = {comp_class_number}"
        f" WHERE class_number = {class_number}"
      )
      # Update related component only if it is not the only one
      if len(related_components) > 1:
        conn.execute(f"UPDATE Class SET related_component_1 = {class_number}"
          f" WHERE class_number = {comp_class_number}"
        )
  # If a class is online, then its related_component_1 must match the section number of its matching related_component_1.
  elif "ONLINE" in primary['campus']:
    return
  else:
    matching_class_numbers = []
    for first in related_components:
      if first['associated_class'] == primary['associated_class']:
        matching_class_numbers.append(first['class_number'])
    r1_value = 2
    if matching_class_numbers:
      # Update the component's related_component_1 to match the primary's class number
      conn.execute(f"UPDATE Class SET related_component_1 = {class_number}"
        f" WHERE class_number IN ({','.join(map(str, matching_class_numbers))})"
      )
      r1_value = 1
    # Update the primary's {component_type}
    conn.execute(f"UPDATE Class SET {component_type} = {r1_value}"
      f" WHERE class_number = {class_number}"
    )


def set_related_components(conn, primary_components, first_components, second_components):
  """
    Iterates through each primary component and determine the class numbers of its related components.
  """
  # If first_components is empty, exit
  if not first_components:
    return
  for primary in primary_components:
    process_primary_component(conn, primary, first_components, 'related_component_1')
    if second_components:
      process_primary_component(conn, primary, second_components, 'related_component_2')


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
      name = make_string_sql_safe(course['title'], '')
      prerequisites = make_string_sql_safe(course['prerequisites'], '')
      antirequisites = make_string_sql_safe(course['antirequisites'], '')
      print(f"Adding {subject} {catalog_number} into Course table")

      # grabs info for specific course
      course_info = get_course(course_id)
      course_description = course_info['description']
      if course_description:
        course_description = make_string_sql_safe(course_description[:1000], '')
      else:
        course_description = "NULL"

      command = (
        f"INSERT INTO Course VALUES ('{course_id}', '{subject}', '{catalog_number}', "
        f"'{name}', '{course_description}', '{prerequisites}', '{antirequisites}') "
      )
      conn.execute(command)

    print("All Courses are now added")


def populate_class(db):
  """
    Populates Class tables
  """
  # Get all existing courses in the Course table
  with db.connect() as conn:
    all_courses_from_table = conn.execute("SELECT * FROM Course")
    courses = [{
        'subject': dict(row)['subject'],
        'catalog_number': dict(row)['catalog_number']
    } for row in all_courses_from_table]

  print("Grabbing schedule for each course from waterloo api, will take a longggg time")
  courses_schedule = []
  for course in courses:
    schedule = get_course_schedule(course['subject'], course['catalog_number'])
    if schedule:
      courses_schedule += schedule
  
  print("Sucessfully obtained all data, now populating tables")
  with db.connect() as conn:
    # For each lecture, determine its related components and update accordingly
    current_subject, current_catalog_number = '', ''
    primary_components, first_components, second_components = [], [], []
    for schedule in courses_schedule:
      print(f"Adding {schedule} to Class table")
      subject = schedule['subject']
      catalog_number = schedule['catalog_number']
      units = schedule['units']
      class_number = schedule['class_number']
      if current_subject is None:
        current_subject = subject
        current_catalog_number = catalog_number
      elif subject != current_subject or current_catalog_number != catalog_number:
        set_related_components(conn, primary_components, first_components, second_components)
        current_subject = subject
        current_catalog_number = catalog_number
        primary_components, first_components, second_components = [], [], []

      section = schedule['section'].split()
      class_type = section[0]
      section_number = section[1]
      if section_number:
        if section_number[0] == '0':
          primary_components.append(schedule)
        elif section_number[0] == '1':
          first_components.append(schedule)
        else:
          second_components.append(schedule)

      campus = schedule['campus']
      associated_class = schedule['associated_class']
      related_component_1 = make_string_sql_safe(schedule['related_component_1'], '0')
      related_component_2 = make_string_sql_safe(schedule['related_component_2'], '0')
      topic = make_string_sql_safe(schedule['topic'], '')
      term = schedule['term']
      academic_level = schedule['academic_level']

      command = (
        "INSERT INTO Class VALUES ("
        f"'{class_number}', '{subject}', '{catalog_number}', '{units}', "
        f"'{class_type}', '{section_number}', '{campus}', "
        f"'{associated_class}', '{related_component_1}', '{related_component_2}', "
        f"'{topic}', '{term}', '{academic_level}') "
      )
      conn.execute(command)
    set_related_components(conn, primary_components, first_components, second_components)


def populate_classtime(db):
  """
    Populates Classtime tables and Instructor table
    Grabs the schedules for each course at /courses/{subject}/{catalog_number}
  """
  # Get all existing class numbers in the Class table
  db_classes = []
  with db.connect() as conn:
    all_db_classes = conn.execute("SELECT class_number FROM Class")
    db_classes = [dict(row) for row in all_db_classes]

  # Get class schedule for all classes
  all_classes = []
  for db_class in db_classes:
    class_schedule = get_class_schedule(db_class['class_number'])
    all_classes.append(class_schedule)

  print(all_classes)

  # Update to database
  with db.connect() as conn:
    for class_ in all_classes:
      class_time = class_['classes'][0]
      current_year = class_['last_updated'].split('-')[0]
      class_number = class_['class_number']
      date = class_time['date']
      
      building = class_time['location']['building']
      room = class_time['location']['room']
      start_time = date['start_time'] or "00:00:00"
      end_time = date['end_time'] or "00:00:00"
      weekdays = date['weekdays'] or "NULL"

      # Populates Instructor table
      instructor_id = None
      if class_time['instructors']:
        instructor_name = make_string_sql_safe(class_time['instructors'][0], '')
        # If instructor exists, don't insert. Otherwise, insert
        instructor_id = conn.execute(
            f"SELECT id FROM Instructor WHERE name = '{instructor_name}'"
        ).first()
        if instructor_id is None:
          conn.execute(
            f"INSERT INTO Instructor (name) VALUES ('{instructor_name}')"
          )
          instructor_id = conn.execute(
            f"SELECT id FROM Instructor WHERE name = '{instructor_name}'"
          ).first()
        instructor_id = f"'{instructor_id[0]}'"
      else:
        instructor_id = "NULL"

      # Not sure how to add null to datetime
      default_date = '1900-01-01'
      start_date = date['start_date'] or default_date
      end_date = date['end_date'] or default_date
      if start_date != default_date:
        start_date = f"{current_year}-{start_date.replace('/', '-')}"
      if end_date != default_date:
        end_date = f"{current_year}-{end_date.replace('/', '-')}"

      is_active = not (date['is_tba'] and date['is_cancelled'] and date['is_closed'])
      command = (
        "INSERT INTO ClassTime (class_number, start_time, end_time, weekdays,"
        "start_date, end_date, is_active, building, room, instructor_id) VALUES ( "
        f"'{class_number}', '{start_time}', "
        f"'{end_time}', '{weekdays}', '{start_date}', "
        f"'{end_date}', '{is_active}', '{building}', "
        f"'{room}', {instructor_id}); "
      )
      conn.execute(command)

  print("Sucessfully added all data")



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", dest="table", required=False)
  parser.add_argument("-u", dest="user", required=False, default="root")
  parser.add_argument("-p", dest="password", required=False, default="tmp")

  arguments = parser.parse_args()

  db = sqlalchemy.create_engine(
    f'postgresql+pg8000://{arguments.user}:{arguments.password}@localhost:5432/schedulemaker')

  table = arguments.table

  if table == "Course":
    print("Populating Course table")
    populate_courses(db)
  elif table == "Class":
    print("Will populate Class table according to the courses in Course table")
    populate_class(db)
  elif table == "Classtime":
    print("Will populate ClassTime table according to the classes in Class table")
    populate_classtime(db)
  else:
    print("Populating all tables")
    populate_courses(db)
    populate_class(db)
    populate_classtime(db)



