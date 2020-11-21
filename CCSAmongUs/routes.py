from flask import render_template, url_for
from CCSAmongUs import app, db
from CCSAmongUs.models import User

@app.route("/")
@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/register")
def register():
	return render_template('register.html')

