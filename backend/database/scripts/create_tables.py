import sqlalchemy
import sys

# Script to create tables in our local database
db = sqlalchemy.create_engine("postgresql+pg8000://root:@localhost:5432/schedulemaker")

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
          print(command)
          if command:
            conn.execute(command)
