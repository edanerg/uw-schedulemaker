import os
from .db_connect import db

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
          'SELECT Class.class_number AS class_nbr, * '
          'FROM ClassTime LEFT JOIN Class ON Class.class_number = ClassTime.class_number '
          f'WHERE ClassTime.class_number = \'{class_num}\''
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

def add_user_schedule(username, class_numbers):
  """
    add to UserSchedule table
  """
  with db.connect() as conn:
    for class_num in class_numbers:
      conn.execute(
          f"INSERT INTO UserSchedule VALUES ('{username}', '{class_num}') ON CONFLICT DO NOTHING;"
      )
    
    conn.close()
