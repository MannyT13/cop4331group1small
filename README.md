# cop4331group1small
Small Group Project for Summer POOD Class


# Setup
- Install Python 2.7 and pip https://bootstrap.pypa.io/get-pip.py <-- run this file with `python get-pip.py`
- Install virtualenv `pip install virtualenv`
- Create a virtualenv for this project in the working directory `virtualenv env`
- Start the virtualenv `source env/bin/activate`
- Inside the env, install the requirements `pip install -r "requirements.txt"`
- Copy the config from the template `cp config.py.template config.py`
- Create the SQLite database by entering the python shell from the working directory and type
`from views import db
db.create_all()`
- Close the python shell and type `export FLASK_APP=views.py`
- Run flask `flask run` and navigate to 127.0.0.1:5000

# Running the app after having everything already setup
- `source env/bin/activate`
- `flask run`
