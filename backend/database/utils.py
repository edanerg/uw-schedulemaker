
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
