import os
import sqlalchemy

# This files sets up connection to SQL database instance

server_env = os.getenv('SERVER_ENV', 'development')


db = sqlalchemy.create_engine("postgresql+pg8000://root:tmp@localhost:5432/schedulemaker")

if (server_env != 'development'):

  # Will need to store and secure the db info somewhere else
  db_drivername = "postgres+pg8000"
  db_user = "root"
  db_pass = "cs348-database"
  db_name = "schedulemaker"
  db_query = {
      "unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format("cs348-database10:us-central1:cs348db")
  }

  db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername=db_drivername,
        username=db_user,
        password=db_pass,
        database=db_name,
        query=db_query,
    ),
  )
