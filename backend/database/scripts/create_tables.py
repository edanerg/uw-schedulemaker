######## Script to create tables in our local database

import sqlalchemy
import sys

db = sqlalchemy.create_engine("postgresql+pg8000://root:tmp@localhost:5432/schedulemaker")

# Open and read the createtables.sql file
path_to_createtables = f'database/sql/createtables.sql'
fd = open(path_to_createtables, 'r')
createtable_file = fd.read()
fd.close()
# Get the createtables commands
createtable_file_commands = createtable_file.split(';')


if __name__ == "__main__":
  with db.connect() as conn:
    for command in createtable_file_commands:
      if command:
        conn.execute(command)

