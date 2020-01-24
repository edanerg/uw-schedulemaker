## 1. Set up your virtual env
pip install pipenv

python3 -m venv venv

source venv/bin/activate

## 2. Install needed modules
pip install -r requirements.txt

## 3. Run backend
FLASK_APP=database flask run

## Some info
Backend Local Port number: 5000 