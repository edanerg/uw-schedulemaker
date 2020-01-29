import os
import sqlalchemy

## This files sets up connection to SQL database instance

server_env = os.getenv('SERVER_ENV', 'development')

db_user = "root"
db_pass = "cs348-database"
db_name = "schedulemaker"
db_query = {
  "unix_socket": "/cloudsql/{}".format("cs348-database10:us-central1:cs348demo-db")
}

if (server_env == 'development'):
  cloud_sql_connection_name = "host=localhost?port=3306"
  db_query = {
      "host": "localhost",
      "port": 3306,
  }

db = sqlalchemy.create_engine(
  sqlalchemy.engine.url.URL(
      drivername="mysql+pymysql",
      username=db_user,
      password=db_pass,
      database=db_name,
      query=db_query,
  ),
)
