import os
from .db_connect import db


############ sql functions for /courses route ###########
def get_filtered_classes(from_time, to_time, weekdays, subject, catalog_number):
  """
    Searches the Classtime table for classes that fit between times from_time and to_time and that
    occurs during the specified weekdays. If subject and catalog_number are specified, classes for this
    specific subject will be outputed
  """
  result = []
  with db.connect() as conn:
    selected_classes = conn.execute(
      "SELECT * FROM Classtime LEFT JOIN "
      "(SELECT Class.class_number AS class_num, Course.subject AS c_subject, Course.catalog_number AS c_catalog, "
      "Class.units AS units, Class.class_type AS class_type, Class.section_number AS section_number, "
      "Course.description AS description, Course.name AS name "
      "FROM Class LEFT JOIN Course ON Course.subject = Class.subject AND Course.catalog_number = Class.catalog_number) "
      "AS CourseAndClass "
      "ON CourseAndClass.class_num = ClassTime.class_number "
      f"WHERE weekdays LIKE '%{weekdays}%' AND c_subject LIKE '%{subject}%' AND c_catalog LIKE '%{catalog_number}%' "
      f"AND start_time >= '{from_time}' AND end_time <= '{to_time}'"
    )
    
    for selected_class in selected_classes:
      class_info = {
        'start_time': selected_class['start_time'].strftime("%H:%M:%S"),
        'end_time': selected_class['end_time'].strftime("%H:%M:%S"),
        'weekdays': selected_class['weekdays'],
        'is_active': selected_class['is_active'],
        'building': selected_class['building'],
        'room': selected_class['room'],
        'subject': selected_class['c_subject'],
        'catalog_number': selected_class['c_catalog'],
        'units': selected_class['units'],
        'class_number': selected_class['class_num'],
        'class_type': selected_class['class_type'],
        'section_number': selected_class['section_number'],
        'description': selected_class['description'],
        'name': selected_class['name'],
      }
      result.append(class_info)
    conn.close()

  return result


############ sql/helper functions for /courses route ###########
def get_courses(subject, catalog_number):
  """
    Returns the info for the course (subject,catalog_number)
  """
  sql_command = "SELECT * FROM Course"
  if subject != '':
    sql_command += f" WHERE subject = '{subject}'"
  if catalog_number != '':
    sql_command += f" AND catalog_number LIKE '{catalog_number}%'" if subject != '' else f" WHERE catalog_number LIKE '{catalog_number}%'"
  with db.connect() as conn:
    all_courses = conn.execute(sql_command)
    result = [dict(row) for row in all_courses]
    print(result)
    conn.close()
  return result


############ sql/helper functions for /user route ###########
def user_profile_actions(data):
  if data['action'] == 'login':
    with db.connect() as conn:
      user = conn.execute(
          f'SELECT * FROM AppUser WHERE username = \'{data["username"]}\'').fetchone()
      print(f"User {data['username']} logging in")
      conn.close()
      return {'user': dict(user.items()) if user else None}

  elif data['action'] == 'signup':
    with db.connect() as conn:
      username = data["username"]
      for c in username:
        if not ('a' <= c <= 'z' or 'A' <= c <= 'Z'):
          return {'result': 'ERROR: username should consist of only lowercase or uppercase letters'}
      academic_level = data["academic_level"] if "academic_level" in data else "undergrad"
      try:
        conn.execute(f'INSERT INTO AppUser (username, academic_level) VALUES (\'{username}\', \'{academic_level}\')')
      except:
        print("problem occured")
        conn.close()
        return {'result': 'ERROR: user already exists'}
      print(f"User {data['username']} signing up")
      conn.close()
      return {'result': 'success'}


############ sql/helper functions for /coursesTaken route ###########
def get_courses_user_taken(username):
  """
    Returns the courses + courses info for the courses that the user took
  """
  result = []
  with db.connect() as conn:
    all_courses = conn.execute(f'SELECT * FROM CoursesTaken, Course WHERE CoursesTaken.username = \'{username}\' AND Course.subject = CoursesTaken.subject AND Course.catalog_number = CoursesTaken.catalog_number').fetchall()
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
    return result


def add_user_course_taken(data):
  """
    Adds courses that the user took in the CoursesTaken table
  """
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


def delete_course_taken(username, subject, catalog_number):
  """
    Deleted the course from CoursesTaken table
  """
  with db.connect() as conn:
    matched_course = conn.execute(f'SELECT * FROM CoursesTaken WHERE username = \'{username}\' AND subject = \'{subject}\' AND catalog_number = \'{catalog_number}\'').fetchone()
    if matched_course is None: return {'result': 'ERROR: You have not taken this course.'}
    try:
      conn.execute(f'DELETE FROM CoursesTaken WHERE username = \'{username}\' AND subject = \'{subject}\' AND catalog_number = \'{catalog_number}\'')
    except:
      return {'result': 'ERROR: Course not uploaded.'}
    conn.close()
    return {'result': 'success'}


############ sql/helper functions for /schedule route ###########
def extract_class_num(user_schedule):
  """
    Extracts class numbers from the users's schedule
  """
  list_class_num = []
  is_class_num = False
  for s in user_schedule.splitlines():
    if is_class_num:
        is_class_num = False
        class_num = int(s)
        list_class_num.append(class_num)
    if s.find('Class Nbr') != -1:
        is_class_num = True
  print(list_class_num)
  return list_class_num

def get_users_classnums(username):
  """
    Returns all the class_numbers for classes that in the user's schedule
  """
  user_class_nums = []
  with db.connect() as conn:
    get_class_nums = conn.execute(
      'SELECT class_number '
      'FROM UserSchedule '
      f"WHERE username = '{username}'"
    )
    user_class_nums = [dict(row)["class_number"] for row in get_class_nums]

    conn.close()
  return user_class_nums


def get_class_schedule(class_numbers):
  """
    Returns the class schedules using list of class_numbers
  """
  classes_list = []
  with db.connect() as conn:
    for class_num in class_numbers:
      all_classes = conn.execute(
          "SELECT Class.class_number AS class_nbr, * "
          "FROM ClassTime LEFT JOIN Class ON Class.class_number = ClassTime.class_number "
          f"WHERE ClassTime.class_number = '{class_num}'; "
      )
      for class_info in all_classes:
        class_info = {
            'id': class_info['class_nbr'],
            'start_time': class_info['start_time'].strftime("%H:%M:%S"),
            'end_time': class_info['end_time'].strftime("%H:%M:%S"),
            'weekdays': class_info['weekdays'],
            'building': class_info['building'],
            'room': class_info['room'],
            'subject': class_info['subject'],
            'catalog_number': class_info['catalog_number'],
            'class_type': class_info['class_type'],
            'topic': class_info['topic'],
            'section_number': class_info['section_number'],
        }
        classes_list.append(class_info)
    conn.close()
  return classes_list


def get_classes_user_can_add(username):
  """
    Returns the classes that fits into the user's schedule
  """
  addable_classes = []
  with db.connect() as conn:
    class_times_info = conn.execute(
      "SELECT weekdays, start_time, end_time "
      "FROM UserSchedule LEFT JOIN ClassTime ON UserSchedule.class_number = ClassTime.class_number "
      f"WHERE username = '{username}';"
    )
    
    class_times_info = [{
      'start_time': row['start_time'].strftime("%H:%M:%S"),
      'end_time': row['end_time'].strftime("%H:%M:%S"),
      'weekdays': row['weekdays'],
    } for row in class_times_info]

    query = ""
    i = 0
    for class_time_info in class_times_info:
      weekday = class_time_info['weekdays']
      start_time = class_time_info['start_time']
      end_time = class_time_info['end_time']

      if i != 0:
        query += "AND "
      query += f"(('{weekday}' NOT LIKE '%' || ClassTime.weekdays || '%' AND ClassTime.weekdays NOT LIKE '%{weekday}%') OR "
      query += f"((ClassTime.end_time < '{start_time}' OR ClassTime.start_time > '{end_time}'))) "
      
      i += 1
    
    addable_classes_query = conn.execute(
      "SELECT class_number "
      "FROM ClassTime "
      f"WHERE {query}"
    )

    addable_classes = [dict(row)['class_number'] for row in addable_classes_query]
    conn.close()
  return addable_classes


def add_user_schedule(username, class_numbers):
  """
    add to UserSchedule table
  """
  with db.connect() as conn:
    for class_num in class_numbers:
      conn.execute(
        f"INSERT INTO UserSchedule SELECT '{username}', '{class_num}' "
        f"WHERE EXISTS (SELECT 1 FROM Class WHERE class_number = '{class_num}') "
        f"ON CONFLICT (username, class_number) DO NOTHING;"
      )
    
    conn.close()
