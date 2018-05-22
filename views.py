import os
from flask import Flask, url_for, redirect, render_template, request, json
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
    email = db.Column(db.String(120), unique=True, nullable=False)
    contacts = db.relationship('Contact', backref='User', lazy=True)

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

# ==================
# Helper Functions
# ==================

def create_user():
	return


def add_contact():
	return


def find_contact():
	return

def remove_contact():
	return

# ==================
# Routing
# ==================

@app.route('/', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	return redirect('login')

@app.route('/index')
def index():
	return render_template('index.html')


