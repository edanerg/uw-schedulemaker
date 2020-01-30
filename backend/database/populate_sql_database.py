from .db_connect import db

# TODO: write function to grab data from waterloo api


with db.connect() as conn:
# conn.execute("commands to update tables") 