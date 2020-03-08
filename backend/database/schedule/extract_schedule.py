import sqlalchemy
import argparse

path_to_file = 'sample_class_schedule.txt'
user_id = 'kc3cheng'

def extract_class_num(path_to_file):
    list_class_num = []
    f = open(path_to_file, 'r')
    user_schedule = f.read()
    user_schedule = str(user_schedule).split("\n")
    is_class_num = False
    for s in user_schedule:
        if is_class_num:
            is_class_num = False
            class_num = int(s)
            list_class_num.append(class_num)
        if s.find('Class Nbr') != -1:
            is_class_num = True
    f.close()
    return list_class_num


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest="table", required=False)
    parser.add_argument("-u", dest="user", required=False, default="root")
    parser.add_argument("-p", dest="password", required=False, default="tmp")

    arguments = parser.parse_args()

    list_class_num = extract_class_num(path_to_file)
    db = sqlalchemy.create_engine(
        f'postgresql+pg8000://{arguments.user}:{arguments.password}@localhost:5432/schedulemaker'
    )
    with db.connect() as conn:
        for class_num in list_class_num:
            command = (
                f"INSERT INTO UserSchedule VALUES ('{user_id}', '{class_num}') "
            )
            conn.execute(command)
    print(f"Sucessfully add {user_id}'s schedule\n")
