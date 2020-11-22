from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from CCSAmongUs.models import Team

class RegisterationForm(FlaskForm):
	teamname = StringField('Team Name', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_teamname(self, teamname):
		team = Team.query.filter_by(teamname=teamname.data).first()
		if team:
			raise ValidationError('Sorry this teamname is taken, Please choose another one')

	def validate_email(self, email):
		team = Team.query.filter_by(email=email.data).first()
		if team:
			raise ValidationError('Sorry this email is taken, Please choose another one')

class LoginForm(FlaskForm):
	teamname = StringField('Team Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')