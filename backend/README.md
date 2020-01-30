https://cs348-database10.appspot.com/courses


## 1. Set up your virtual env
pip install pipenv

python3 -m venv venv

source venv/bin/activate

## 2. Install needed modules
pip install -r requirements.txt

## 3. Run backend
gunicorn --bind 0.0.0.0:8080 app:app

## 4. To connect to the SQL database
Download cloud_sql_proxy in your root folder and execute:

`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348demo-db=tcp:3306`


## 5. To populate our SQL database with Waterloo data using waterloo api
Run `python3 database/populate_sql_database.py`

## Some info
Backend Local Port number: 8080
