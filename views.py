import os
from flask import Flask, url_for, redirect, render_template, request, json, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# ==================
# Models
# ==================

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	contacts = db.relationship('Contact', backref='User', lazy=True)
	pw_hash = db.Column(db.String(256), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)


	def __repr__(self):
		return '<User %r>' % self.username

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	contact_owner = db.Column(db.Integer, db.ForeignKey('user.id'),
			nullable=False)
	name = db.Column(db.String(80), unique=False, nullable=False)
	number = db.Column(db.Integer)

	def __init__(self, contact_owner, name, number):
		self.contact_owner = contact_owner
		self.name = name
		self.number = number

# ==================
# Helper Functions
# ==================

def find_contact(name, number):
	return

def remove_contact():
	return

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in_user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================
# Routing
# ==================

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = User.query.filter_by(username=request.form['username']).first()
		if user is None or not user.check_password(request.form['password']):
			flash('Username or password incorrect')
			return redirect('login')

		else:
			session['logged_in_user'] = user.id
			return redirect('/')

	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('logged_in_user')
	return redirect('login')

@app.route('/register', methods=['GET', 'POST'])
def register():
	# If user submitted the form
	if request.method == 'POST':
		# Check to see if username exists already
		check_username = User.query.filter_by(username=request.form['username']).first()
		if check_username is None:
			# Create the new user
			new_user = User(request.form['username'], request.form['password'])

			db.session.add(new_user)
			db.session.commit()
			session['logged_in_user'] = new_user.id

			return redirect('/')
		else:
			flash('Username already exists')
			return redirect('register')
	return render_template('registration.html')

@app.route('/')
@login_required
def index():
	return render_template('index.html')


