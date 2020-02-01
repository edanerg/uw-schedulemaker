https://cs348-database10.appspot.com/courses


## 1. Install virtual env for python(only do once if you don't have pipenv downloaded)
pip install pipenv

## 2. Activate virtual environment
python3 -m venv venv
source venv/bin/activate

## 3. Install needed modules
pip install -r requirements.txt

## 4. Run backend
gunicorn --bind 0.0.0.0:8080 app:app

## 5. To connect to SQL posgres
Download cloud_sql_proxy in your root folder and execute:

For development database:
`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348db=tcp:3306`

For development database:
`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348-production-db=tcp:3306`

## 6. To populate our SQL database with Waterloo data using waterloo api
Run `python3 database/populate_sql_database.py`

## Some info
Backend Local Port number: 8080
