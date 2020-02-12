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

### Steps: 
`brew install postgresql`

`pg_ctl -D /usr/local/var/postgres start && brew services start postgresql`

`psql postgres`

Our database name is schedulemaker, type in this when posgres started:

postgres=# `CREATE DATABASE schedulemaker`


#### To run scripts for local database:

### You can try this:
python3 ./database/scripts/execute_sql.py -f createtables -u yourUsername -p yourPassword

### To Populate all data into local database:
python3 ./database/scripts/populate_tables.py -u yourUsername -p yourPassword

### To Populate specific table into local database:
python3 ./database/scripts/populate_tables.py -t 'table_you_want_to_populate' -u yourUsername -p yourPassword


### For connecting to production database:
Download cloud_sql_proxy in your root folder and execute:

For development database:

`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348db=tcp:3306`

For development database:

`./cloud_sql_proxy -instances=cs348-database10:us-central1:cs348-production-db=tcp:3306`
