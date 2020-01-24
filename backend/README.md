https://cs348-database10.appspot.com/courses


## 1. Set up your virtual env
pip install pipenv

python3 -m venv venv

source venv/bin/activate

## 2. Install needed modules
pip install -r requirements.txt

## 3. Run backend
gunicorn --bind 0.0.0.0:8080 app:app

## Some info
Backend Local Port number: 8080
