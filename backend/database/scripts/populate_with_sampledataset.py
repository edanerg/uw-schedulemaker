######## Script to populate tables with sample dataset database

import sqlalchemy
import sys

db = sqlalchemy.create_engine("postgresql+pg8000://root:tmp@localhost:5432/schedulemaker")

# Open and read the createtables.sql file
path_to_sampledataset = f'database/sql/sampledataset.sql'
fd = open(path_to_sampledataset, 'r')
sampledataset_file = fd.read()
fd.close()
# Get the createtables commands
sampledataset_file_commands = sampledataset_file.split(';')


if __name__ == "__main__":
  with db.connect() as conn:
    for command in sampledataset_file_commands:
      if command:
        conn.execute(command)

