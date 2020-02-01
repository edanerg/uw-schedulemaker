from db_connect import db

# Script to create tables in the database

# Open and read the createtables.sql file
path_to_createtables = f'./database/sql/createtables.sql'
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
