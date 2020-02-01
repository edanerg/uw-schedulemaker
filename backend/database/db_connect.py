import os
import sqlalchemy

# This files sets up connection to SQL database instance

server_env = os.getenv('SERVER_ENV', 'development')

# Will need to store and secure the db info somewhere else
db_drivername = "postgres+pg8000"
db_user = "root"
db_pass = "cs348-database"
db_name = "schedulemaker"
db_query = {
    "unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format("cs348-database10:us-central1:cs348db")
}

if (server_env == 'development'):
  db_query = {
      "host": "localhost",
      "port": 3307,
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
