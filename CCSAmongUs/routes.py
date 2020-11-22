from flask import render_template, url_for, flash, redirect
from CCSAmongUs import app, db
from CCSAmongUs.forms import RegisterationForm, LoginForm
from CCSAmongUs.models import Team, User, Questions
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('terminal'))
	form = LoginForm()
	if form.validate_on_submit():
		team = Team.query.filter_by(teamname=form.teamname.data).first()
		if team and team.password == form.password.data:
			login_user(team)
			return redirect(url_for('terminal'))
		else:
			flash('Unsuccessful attempt', 'danger')
	return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('terminal'))
	form = RegisterationForm()
	if form.validate_on_submit():
		details = Team(teamname=form.teamname.data, email=form.email.data, password=form.password.data)
		db.session.add(details)
		db.session.commit()
		login_user(details)
		flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
		return redirect(url_for('memberRegister'))
	return render_template('register.html', form=form)

@login_required
@app.route("/memberRegister")
def memberRegister():
	form = RegisterationForm()
	if form.validate_on_submit():
		user = Team(teamname=form.teamname.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
		return redirect(url_for('login'))
	return render_template('memberRegister.html', form=form)

@login_required
@app.route("/terminal")
def terminal():
	return render_template('terminal.html')

