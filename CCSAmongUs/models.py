from datetime import datetime
from CCSAmongUs import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Team.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	name = db.Column(db.String(40), nullable=False)
	rollnumber = db.Column(db.Integer, nullable=False, unique=True)
	team = db.Column(db.String(20), db.ForeignKey('team.teamname'), nullable=False) 
	def __repr__(self):
		return f"User('{self.name}', '{self.rollnumber}', '{self.team}')"

class Team(db.Model, UserMixin): 
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	teamname = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	coins = db.Column(db.Integer)
	score = db.Column(db.Integer)
	check = db.Column(db.Integer, default=0)
	db.relationship('Post', backref='team', lazy=True)

	def __repr__(self):
		return f"Team('{self.teamname}', '{self.email}')"

class Questions(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	question = db.Column(db.String(1000), nullable=False)
	answer = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return f"Question('{self.question}', '{self.answer}')"