import os
from flask import Flask
from flask_restful import Resource, Api
from json import dumps
from flask_cors import CORS
import sqlalchemy

app = Flask(__name__)
api = Api(app)
CORS(app)
sql_folder = os.getcwd()

# Open and read the createtables.sql file
path_to_createtables = f'{sql_folder}/database/sql/createtables.sql'
fd = open(path_to_createtables, 'r')
createtable_file = fd.read()
fd.close()
createtable_file_commands = createtable_file.split(';')


# TODO: adding the username, passwords, etc is not safe. Will have to move it somewhere else in the future
db_user = "root"
db_pass = "cs348-database"
db_name = "schedulemaker"
cloud_sql_connection_name = "cs348-database10:us-central1:cs348demo-db"

# Connection to database
# For local testing use this:
db = sqlalchemy.create_engine(
    "mysql+pymysql://root:cs348-database@127.0.0.1/schedulemaker?host=localhost?port=3306"
)

# When deploying to production uncomment this:
# (will clean this up after so that we don't have to comment/uncomment code for production)
# db = sqlalchemy.create_engine(
#     sqlalchemy.engine.url.URL(
#       drivername="mysql+pymysql",
#       username=db_user,
#       password=db_pass,
#       database=db_name,
#       query={
#         "unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)
#       },
#     ),
# )

# create_tables() will execute when frontend does it's first api request
# can add an admin button to do this
@app.before_first_request
def create_tables():
    with db.connect() as conn:
        # Execute every command from the createtables file
        for command in createtable_file_commands:
            if command:
              conn.execute(command)


# TODO: Change to receive data from database
class Courses(Resource):
    def get(self):
        return {'courses': ['cs', 'maths', 'biology']}


class Main(Resource):
    def get(self):
        return "Hi there!"


# TODO: add more routes
api.add_resource(Main, '/')
api.add_resource(Courses, '/courses')
