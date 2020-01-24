## Set up your virtual env
pip install pipenv
python3 -m venv venv
source venv/bin/activate

## Install needed modules
pip install -r requirements.txt

## Run backend
FLASK_APP=database flask run