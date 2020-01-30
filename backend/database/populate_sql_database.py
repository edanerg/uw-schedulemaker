import requests
# from .db_connect import db

# TODO: write function to grab data from waterloo api

# write function to add data to sql database:
# with db.connect() as conn:
# conn.execute("commands to update tables") 

if __name__ == "__main__":
  #  Example of a get request to the https://xkcd.com/1906/ url
  r = requests.get('https://xkcd.com/1906/')
  print(r.text)

  print("test")
