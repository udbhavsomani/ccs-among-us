from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from CCSAmongUs.models import Team, User, Questions

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

	def validate_teamname(self, teamname):
		team = Team.query.filter_by(teamname=teamname.data).first()
		if team == None:
			raise ValidationError('This teamname is not registered.')
		# print(team)
		if team.password != self.password.data:
			raise ValidationError('Incorrect Password.')

class MemberRegisterForm(FlaskForm):
	member1 = StringField('Member 1 name', validators=[DataRequired()])
	member2 = StringField('Member 2 name', validators=[DataRequired()])
	member3 = StringField('Member 3 name')
	rollnumber1 = StringField('Member 1 Roll No.', validators=[DataRequired()])
	def validate_rollnumber1(self, rollnumber1):
		user = User.query.filter_by(rollnumber=rollnumber1.data).first()
		if user:
			raise ValidationError('Member 1 is already registered.')
	rollnumber2 = StringField('Member 2 Roll No.', validators=[DataRequired()])
	def validate_rollnumber2(self, rollnumber2):
		user = User.query.filter_by(rollnumber=rollnumber2.data).first()
		if user:
			raise ValidationError('Member 2 is already registered.')
	rollnumber3 = StringField('Member 3 Roll No.')
	def validate_rollnumber3(self, rollnumber3):
		user = User.query.filter_by(rollnumber=rollnumber3.data).first()
		if user:
			raise ValidationError('Member 3 is already registered.')
	submit = SubmitField('Register')
	