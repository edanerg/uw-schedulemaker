######## Script to purge tables in our local database

import sqlalchemy

db = sqlalchemy.create_engine("postgresql+pg8000://root:tmp@localhost:5432/schedulemaker")

# Open and read the createtables.sql file
path_to_purgetables = 'database/sql/purgetables.sql'
fd = open(path_to_purgetables, 'r')
purgetable_file = fd.read()
fd.close()
# Get the createtables commands
purgetable_file_commands = purgetable_file.split(';')

if __name__ == "__main__":
    with db.connect() as conn:
        for command in purgetable_file_commands:
          print(command)
          if command:
            conn.execute(command)

