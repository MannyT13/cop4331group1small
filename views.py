import os
from flask import Flask, url_for, redirect, render_template, request, json, session, flash, jsonify
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
	first_name = db.Column(db.String(80), unique=False, nullable=False)
	last_name = db.Column(db.String(80), unique=False, nullable=False)
	email_address = db.Column(db.String(80), unique=False, nullable=False)
	street_address1 = db.Column(db.String(80), unique=False, nullable=False)
	street_address2 = db.Column(db.String(80), unique=False, nullable=True)
	phone_number = db.Column(db.String(15), unique=False, nullable=False)
	city = db.Column(db.String(80), unique=False, nullable=False)
	zip_code = db.Column(db.Integer)

	def __init__(self, contact_owner, first_name, last_name, email_address, street_address1, street_address2, phone_number, city, zip_code):
		self.contact_owner = contact_owner
		self.first_name = first_name
		self.last_name = last_name
		self.email_address = email_address
		self.street_address1 = street_address1
		self.street_address2 = street_address2
		self.phone_number = phone_number
		self.city = city
		self.zip_code = zip_code

	def serialize(self):
		return {
				'id' : str(self.id),
				'contact_owner': str(self.contact_owner),
				'first_name': str(self.first_name),
				'last_name': str(self.last_name),
				'email': str(self.email_address),
				'address1': str(self.street_address1),
				'address2': str(self.street_address2),
				'phone' : str(self.phone_number),
				'city': str(self.city),
				'zip': str(self.zip_code)
			}



# ==================
# Helper Functions
# ==================
"""
def find_contact(name):
	contacts = Contact.query.filter(Contact.first_name.startswith(name)).all()
	error_message = "Contact not found"
	if contacts:
		error_message = None
	return (contacts, error_message)
"""
def find_contact(name):
	contact_list = []
	error_message = "Contact not found"
	# Search by name
	contact_list.append(Contact.query.filter(Contact.first_name.find(name) != -1).all())
	contact_list.append(Contact.query.filter(Contact.last_name.find(name) != -1).all())
	if not contact_list:
		error_message = None
	return (contact_list, error_message)


def remove_contact(name):
	contact = Contact.query.filter_by(name=first_name).first()
	if contact:
		db.session.delete(contact)
		db.session.commit()
		return True
	return False 

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

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
	if request.method == 'POST':
		new_contact = Contact(session['logged_in_user'],request.form['first_name'],
							  request.form['last_name'],request.form['email'],
							  request.form['address1'],request.form['address2'],
							  request.form['phone'],request.form['city'],
							  request.form['zipcode'])
		db.session.add(new_contact)
		db.session.commit()
		db.session.flush()

	return jsonify(new_contact.serialize())

@app.route('/delete_contact', methods=['GET', 'POST'])
def delete_contact():

	data =int(request.get_json())
	print(type(data))
	cnt = db.session.query(Contact).filter(Contact.id == data).first()
	print(cnt)
	
	if cnt:
		if request.method == 'POST':
			db.session.delete(cnt)
			db.session.commit()

	return render_template('homepage.html')
	
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
	contacts = Contact.query.filter_by(contact_owner=int(session['logged_in_user'])).all()
	return render_template('homepage.html',contacts=contacts)


