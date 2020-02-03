import sqlalchemy
import re
import argparse
from sys import argv


def execute(filename, user, password):
  db = sqlalchemy.create_engine(f'postgresql+pg8000://{user}:{password}@localhost:5432/schedulemaker')

  # Open and read the createtables.sql file
  path_to_sql = f'database/sql/{filename}.sql'
  fd = open(path_to_sql, 'r')
  sql = fd.read()
  fd.close()

  # Get the createtables commands
  sql = re.sub(r'(?m)^(--).*\n?', "", sql)
  sql_commands = sql.split(';')

  with db.connect() as conn:
    for command in sql_commands:
      if command:
        conn.execute(command)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", dest="file", required=True)
  parser.add_argument("-u", dest="user", required=False, default="root")
  parser.add_argument("-p", dest="password", required=False, default="tmp")
  arguments = parser.parse_args()
  execute(arguments.file, arguments.user, arguments.password)
