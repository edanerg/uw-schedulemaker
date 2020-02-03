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
### For connecting to local database:
I followed this tutorial: https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb

Which sums up to this:

`brew install postgresql`

`pg_ctl -D /usr/local/var/postgres start && brew services start postgresql`

`psql postgres`

Our database name is schedulemaker, type in this when posgres started:

postgres=# `CREATE DATABASE schedulemaker`


#### To run the create_tables script:

python3 ./database/scripts/create_tables.py

### Alex: Above might not work if you have different db username or the sql contains comments
### You can try this:

python3 ./database/scripts/execute_sql.py -f createtables -u yourUsername -p yourPassword

### For connecting to production database:
Download cloud_sql_proxy in your root folder and execute:

For development database:

`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348db=tcp:3306`

For development database:

`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348-production-db=tcp:3306`
