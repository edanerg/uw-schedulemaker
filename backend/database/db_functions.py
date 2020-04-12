import os
import re
from .prereq import check_prereq, is_antireq
from .db_connect import db
from sqlalchemy import text

############ sql functions for /classes route ###########
def get_filtered_classes(from_time, to_time, weekdays, subject, catalog_number):
  """
    Searches the Classtime table for classes that fit between times from_time and to_time and that
    occurs during the specified weekdays. If subject and catalog_number are specified, classes for this
    specific subject will be outputed
  """
  result = []
  with db.connect() as conn:
    selected_classes = conn.execute( text(
      "SELECT * FROM (Classtime LEFT JOIN "
      "(SELECT Class.class_number AS class_num, Course.subject AS c_subject, Course.catalog_number AS c_catalog, "
      "Class.units AS units, Class.class_type AS class_type, Class.section_number AS section_number, "
      "Course.description AS description, Course.name AS course_name "
      "FROM Class LEFT JOIN Course ON Course.subject = Class.subject AND Course.catalog_number = Class.catalog_number) "
      "AS CourseAndClass "
      "ON CourseAndClass.class_num = ClassTime.class_number) "
      "LEFT JOIN Instructor ON Classtime.instructor_id = Instructor.id "
      f"WHERE weekdays LIKE :weekdays AND c_subject LIKE :subject AND c_catalog LIKE :catalog_number "
      f"AND start_time >= :from_time AND end_time <= :to_time"),
        {
          'weekdays': f'%{weekdays}%', "subject": f'%{subject}%', "catalog_number": f'%{catalog_number}%',
          'from_time': from_time, 'to_time': to_time
        }
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
        'name': selected_class['course_name'],
        'instructor': selected_class['name'],
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
    sql_command += f" WHERE subject = :subject"
  if catalog_number != '':
    sql_command += f" AND catalog_number LIKE :catalog_number" if subject != '' else f" WHERE catalog_number LIKE :catalog_number"
  with db.connect() as conn:
    all_courses = conn.execute(
        text(sql_command), {'catalog_number': f'{catalog_number}%', "subject": subject})
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
        conn.execute(text(f'INSERT INTO AppUser (username, academic_level) VALUES (:username, :academic_level)'),
          username = username, academic_level = academic_level)
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
    all_courses = conn.execute(
      text("SELECT * FROM CoursesTaken, Course WHERE CoursesTaken.username = :username "
      " AND Course.subject = CoursesTaken.subject AND Course.catalog_number = CoursesTaken.catalog_number"), username = username).fetchall()
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
    matched_course = conn.execute(
      text("SELECT * FROM Course WHERE Course.subject = :subject "
      "AND Course.catalog_number = :catalog_number"),
      subject = data["subject"], catalog_number = data["catalog_number"]).fetchone()
    if matched_course is None: return {'result': 'ERROR: No Such Course.'}
    matched_course = dict(matched_course.items())
    try:
      conn.execute(
        text("INSERT INTO CoursesTaken VALUES (:username, :subject, :catalog_number)"),
        username = data["username"], subject = matched_course["subject"], 
        catalog_number = matched_course["catalog_number"])
    except:
      return {'result': 'ERROR: Course Already Exists.'}
    conn.close()
    return {'result': 'success', 'course': matched_course}


def delete_course_taken(username, subject, catalog_number):
  """
    Deleted the course from CoursesTaken table
  """
  with db.connect() as conn:
    matched_course = conn.execute(
      text("SELECT * FROM CoursesTaken WHERE username = :username AND subject = :subject AND catalog_number = :catalog_number"),
      username = username, subject = subject, catalog_number = catalog_number).fetchone()
    if matched_course is None: return {'result': 'ERROR: You have not taken this course.'}
    try:
      conn.execute(
        text("DELETE FROM CoursesTaken WHERE username = :username AND subject = :subject AND catalog_number = :catalog_number"),
        username = username, subject = subject, catalog_number = catalog_number)
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
      text("SELECT class_number FROM UserSchedule WHERE username = :username;"),
      username = username
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
          text("SELECT Class.class_number AS class_nbr, * "
          "FROM ClassTime LEFT JOIN Class ON Class.class_number = ClassTime.class_number "
          "WHERE ClassTime.class_number = :class_num"), class_num = class_num
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
            'section_number': class_info['section_number'],
            'topic': class_info['topic'],
            'academic_level': class_info['academic_level'],
            'campus': class_info['campus'],
            'rel_1': class_info['related_component_1'],
            'rel_2': class_info['related_component_2'],
        }
        classes_list.append(class_info)
    conn.close()
  return classes_list


def filter_and_extract_classes(condition, components):
  """
    Returns an array of pairs of class numbers and section numbers of components that 
    satisfy the condition
  """
  class_nums = []
  for comp in components:
    if condition(comp):
      class_nums.append((comp['class_nbr'], comp['section_number']))
  return class_nums


def allowed_class_nums(primary_components, first_components, second_components):
  """
    Returns all addable classes after removing any components that did not have their other matching components.
  """
  allowed_primaries, allowed_firsts, allowed_seconds = [], set(), set()
  open_firsts = filter(lambda comp: comp['related_component_1'] == 99, first_components)
  open_firsts = list(map(lambda first: (first['class_nbr'], first['section_number']), open_firsts))
  open_seconds = filter(lambda comp: comp['related_component_1'] == 99, second_components)
  open_seconds = list(map(lambda second: (second['class_nbr'], second['section_number']), open_seconds))
  if not primary_components:
    return []
  for primary in primary_components:
    r1_value = primary['related_component_1']
    r2_value = primary['related_component_2']
    # If class is supposed to have first or second components but there aren't any, skip
    if (r1_value != 0 and not first_components) or (r2_value != 0 and not second_components):
      continue
    class_number = primary['class_nbr']
    if r1_value == 1:
      matching_firsts = filter_and_extract_classes(lambda comp:
        comp['related_component_1'] == class_number, first_components)
      # If class is supposed to have matching first components but none matched, skip
      if not matching_firsts:
        continue
      allowed_firsts.update(matching_firsts)
    elif r1_value == 2:
      # If class is supposed to have any open first component but there aren't any, skip
      if not open_firsts:
        continue
    elif r1_value != 0:
      matching_first = filter_and_extract_classes(lambda comp:
        comp['class_nbr'] == r1_value, first_components)
      # If there is exactly one matching first component but it isn't included, skip
      if not matching_first:
        continue
      allowed_firsts.update(matching_first)
    if r2_value == 1:
      matching_seconds = filter_and_extract_classes(lambda comp:
        comp['related_component_1'] == class_number, second_components)
      if not matching_seconds:
        continue
      allowed_seconds.update(matching_seconds)
    elif r2_value == 2:
      if not open_seconds:
        continue
    elif r2_value != 0:
      matching_second = filter_and_extract_classes(lambda comp:
        comp['class_nbr'] == r2_value, second_components)
      if not matching_second:
        continue
      allowed_seconds.update(matching_second)
    allowed_primaries.append(class_number)
  if not allowed_primaries:
    return []
  # Add the open components and sort by section number
  allowed_firsts.update(open_firsts)
  allowed_firsts = map(lambda first: first[0], 
    sorted(allowed_firsts, key = (lambda comp: comp[1])))
  allowed_seconds.update(open_seconds)
  allowed_seconds = map(lambda sec: sec[0], 
    sorted(allowed_seconds, key = (lambda comp: comp[1])))
  return allowed_primaries + list(allowed_firsts) + list(allowed_seconds)


def remove_incomplete_components(addable_classes):
  """
    Returns all addable classes after removing any primary components that didn't have their
    matching related components.
  """
  finalized_class_nums = []
  current_subject = ''
  current_catalog_number = ''
  primary_components, first_components, second_components = [], [], []
  for addable_class in addable_classes:
    subject = addable_class['subject']
    catalog_number = addable_class['catalog_number']
    if current_subject is None:
        current_subject = subject
        current_catalog_number = catalog_number
    elif subject != current_subject or current_catalog_number != catalog_number:
      finalized_class_nums += allowed_class_nums(primary_components, first_components, second_components)
      current_subject = subject
      current_catalog_number = catalog_number
      primary_components, first_components, second_components = [], [], []
    section_number = addable_class['section_number']
    if len(section_number) > 0:
      if section_number[0] == '0':
        primary_components.append(addable_class)
      elif section_number[0] == '1':
        first_components.append(addable_class)
      else:
        second_components.append(addable_class)
  finalized_class_nums += allowed_class_nums(primary_components, first_components, second_components)
  return finalized_class_nums


def get_classes_user_can_add(username):
  """
    Returns the class numbers of classes that fits into the user's schedule
  """
  addable_classes = []
  with db.connect() as conn:
    class_times_info = conn.execute(
      text("SELECT weekdays, start_time, end_time "
      "FROM UserSchedule LEFT JOIN ClassTime ON UserSchedule.class_number = ClassTime.class_number "
      f"WHERE username = :username;"), {'username': username}
    )
    #get user's academic level
    user_info = conn.execute(
      text("SELECT academic_level FROM AppUser WHERE username = :username;"), {'username': username}
    )
    academic_level = [dict(row)['academic_level'] for row in user_info][0]
    
    # get user's classes' days and times
    class_times_info = [{
      'start_time': row['start_time'].strftime("%H:%M:%S"),
      'end_time': row['end_time'].strftime("%H:%M:%S"),
      'weekdays': row['weekdays'],
    } for row in class_times_info]

    # get courses that the user is currently taking and has already taken
    current_courses = conn.execute(
      text("SELECT DISTINCT subject, catalog_number FROM UserSchedule NATURAL JOIN Class "
           "WHERE username = :username;"), {'username': username}
    )
    courses_taken = conn.execute(
      text("SELECT subject, catalog_number FROM CoursesTaken "
           "WHERE username = :username;"), {'username': username}
    )
    current_courses = [(row['subject'], row['catalog_number']) for row in current_courses]
    courses_taken = [(row['subject'], row['catalog_number']) for row in courses_taken]
    current_courses += courses_taken
    total_courses = str(current_courses)
    total_courses = total_courses[1:len(total_courses)-1] # removes square brackets

    query = ""
    for class_time_info in class_times_info:
      weekday = class_time_info['weekdays']
      start_time = class_time_info['start_time']
      end_time = class_time_info['end_time']
      query += f"(('{weekday}' NOT LIKE '%' || ClassTime.weekdays || '%' AND ClassTime.weekdays NOT LIKE '%{weekday}%') OR "
      query += f"((ClassTime.end_time < '{start_time}' OR ClassTime.start_time > '{end_time}'))) AND "
    
    query += f"(subject, catalog_number) NOT IN (VALUES {total_courses}) AND "
    addable_classes_query = conn.execute(
      "SELECT ClassTime.class_number as class_nbr, Class.subject, Class.catalog_number, "
      "Class.section_number, Class.related_component_1, Class.related_component_2 "
      "FROM ClassTime LEFT JOIN Class ON ClassTime.class_number = Class.class_number "
      f"WHERE {query} academic_level = '{academic_level}' "
      "ORDER BY subject, catalog_number, section_number; "
    )

    addable_classes = [dict(row) for row in addable_classes_query]
    addable_courses = [(row['subject'], row['catalog_number']) for row in addable_classes]
    addable_courses = list(set([i for i in addable_courses]))  # remove duplicates
    addable_courses = str(addable_courses)
    addable_courses = addable_courses[1:len(addable_courses)-1]

    get_total_courses_antireq_quary = conn.execute(
      "SELECT subject, catalog_number, antirequisites "
      "FROM Course "
      f"WHERE (Course.subject, Course.catalog_number) IN (VALUES {total_courses}); "
    )

    total_courses_antireq = [dict(row) for row in get_total_courses_antireq_quary]

    if len(addable_courses) > 0:
      get_addable_classes_prereq_quary = conn.execute(
        "SELECT subject, catalog_number, prerequisites "
        "FROM Course "
        f"WHERE (Course.subject, Course.catalog_number) IN (VALUES {addable_courses}); "
      )
      addable_classes_prereq = {row['subject']+row['catalog_number']: row['prerequisites'] for row in get_addable_classes_prereq_quary}

    # remove classes in addable_classes that are anti-requisites to any of the courses in total courses
    for addable_class in reversed(addable_classes):
      for course in total_courses_antireq:
        added_course = addable_class['subject']+addable_class['catalog_number']
        past_course_antireq = course['antirequisites']
        if is_antireq(added_course, past_course_antireq):
          addable_classes.remove(addable_class)
          break

    current_courses = [row[0]+row[1] for row in current_courses] # list of courses taken by the user

    # remove classes in addable_classes if the user does not satisfy the classes'prerequisites
    for addable_class in reversed(addable_classes):
      added_course = addable_class['subject']+addable_class['catalog_number']
      added_course_prereq = addable_classes_prereq.get(added_course)
      assert(added_course_prereq is not None)
      if not check_prereq(current_courses, added_course_prereq):
        addable_classes.remove(addable_class)


    addable_classes = remove_incomplete_components(addable_classes)
    print(addable_classes)
    conn.close()
  return addable_classes


def add_user_schedule(username, class_numbers):
  """
    add to UserSchedule table
  """
  with db.connect() as conn:
    for class_num in class_numbers:
      conn.execute(
        text("INSERT INTO UserSchedule SELECT :username, :class_num "
        "WHERE EXISTS (SELECT 1 FROM Class WHERE class_number = :class_num) "
        "ON CONFLICT (username, class_number) DO NOTHING;"),
        {'username': username, 'class_num': class_num}
      )
    
    conn.close()


def remove_from_user_schedule(username, class_numbers):
  """
    remove class_numbers from UserSchedule table
  """
  with db.connect() as conn:
    for class_num in class_numbers:
      conn.execute(
          text("DELETE FROM UserSchedule "
               "WHERE class_number = :class_num AND username = :username "),
          {'class_num': class_num, 'username': username}
      )

    conn.close()

############ sql/helper functions for /instructor route ###########
def get_instructor_classes(instructor_name):
  with db.connect() as conn:
    instructor_name = instructor_name or ""
    instructor_name = re.sub('[^a-zA-z]', ' ', instructor_name).split()
    regex = "(" + "|".join(instructor_name) + ")" if len(instructor_name) > 0 else ".*"
    classes = conn.execute(
      text("SELECT Class.class_number AS class_nbr, Instructor.name AS inst_name, * "
           "FROM Instructor, ClassTime, Class, Course "
           "WHERE Instructor.name ~* :pattern and ClassTime.instructor_id = Instructor.id "
           "and ClassTime.class_number = Class.class_number and Course.subject = Class.subject and Course.catalog_number = Class.catalog_number;"),
      {'pattern': f'{regex}'}
    )
    classes_list = []
    for class_info in classes:
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
        'academic_level': class_info['academic_level'],
        'description': class_info['description'],
        'instructor': class_info['inst_name'],
      }
      classes_list.append(class_info)
    conn.close()
  return classes_list

