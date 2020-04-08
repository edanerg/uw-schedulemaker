import os
import sqlalchemy

# This files sets up connection to SQL database instance
db = sqlalchemy.create_engine("postgresql+pg8000://root:tmp@localhost:5432/schedulemaker")
