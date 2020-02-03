import requests
import sqlalchemy

# TODO: write function to grab data from waterloo api

# write function to add data to sql database:
# Fill in all course to Course relation

db = sqlalchemy.create_engine("postgresql+pg8000://root:tmp@localhost:5432/schedulemaker")
params = {'key': '6642768b60d4b5dcde0d2d10db5500fa'}

if __name__ == "__main__":
    r = requests.get('https://api.uwaterloo.ca/v2/courses.json', params=params)
    data = r.json()['data']
    with db.connect() as conn:
        for courses in data:
            course_id = "'" + str(courses['course_id']) + "'"
            subject = "'" + str(courses['subject']) + "'"
            catalog_num = "'" + str(courses['catalog_number']) + "'"
            name = str(courses['title'])
            i_quote = name.find("'")
            if i_quote != - 1:
                name = str(name[0:i_quote+1]) + "'" + str(name[i_quote+1:]) # put escape char after each ' in name
                i_quote += 2
                while i_quote < len(name):
                    i_quote = name.find("'", i_quote)
                    if i_quote == -1: break
                    name = str(name[0:i_quote + 1]) + "'" + str(name[i_quote + 1:])
                    i_quote += 2
            name = "'" + name + "'"
            course_descrip = "'" + "NULL" + "'"
            command = "INSERT INTO Course VALUES (" + course_id + "," + subject + "," + catalog_num + "," + name + "," + \
                      course_descrip + ")"
            conn.execute(command)

