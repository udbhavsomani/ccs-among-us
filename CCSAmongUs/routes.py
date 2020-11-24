from flask import render_template, url_for, flash, redirect, request, jsonify
from CCSAmongUs import app, db
from CCSAmongUs.forms import RegisterationForm, LoginForm, MemberRegisterForm
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
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('terminal'))
    form = RegisterationForm()
    if form.validate_on_submit():
        details = Team(teamname=form.teamname.data,
                       email=form.email.data, password=form.password.data)
        db.session.add(details)
        db.session.commit()
        login_user(details)
        flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
        return redirect(url_for('memberRegister'))
    return render_template('register.html', form=form)


@app.route("/memberRegister", methods=['GET', 'POST'])
@login_required
def memberRegister():
    form = MemberRegisterForm()
    if current_user.check:
        return redirect(url_for('terminal'))
    if form.validate_on_submit():
        teamname = current_user.teamname
        user1 = User(name=form.member1.data,
                     rollnumber=form.rollnumber1.data, team=teamname)
        user2 = User(name=form.member2.data,
                     rollnumber=form.rollnumber2.data, team=teamname)
        if form.member3.data and form.rollnumber3.data:
            user3 = User(name=form.member3.data,
                         rollnumber=form.rollnumber3.data, team=teamname)
            db.session.add_all([user1, user2, user3])
        else:
            db.session.add_all([user1, user2])
        current_user.check = 1
        db.session.commit()
        return redirect(url_for('terminal'))
    return render_template('memberRegister.html', form=form)


@app.route("/terminal", methods=['GET', 'POST'])
@login_required
def terminal():
    if request.method == 'POST' and request.form['command'] == 'get_teamname':
        return jsonify({'user': current_user.teamname})

    if request.method == 'POST' and request.form['command'] == 'get_coins':
        return jsonify({'coins': current_user.coins})

    if request.method == "POST" and request.form['command'] == 'logout':
        logout_user()
        return jsonify({'url': '/login'})

    if request.method == "POST" and request.form['command'] == 'transact':
        coins = request.form['amount']
        team2 = request.form['team2']
        team = Team.query.filter_by(teamname=team2).first()

        if team == None:
            return jsonify({'error': 'Team does not exists!'})
        if team.teamname == current_user.teamname:
            return jsonify({'error': 'Cannot send coins to self!'})
        else:
            try:
                if current_user.coins < int(coins):
                    return jsonify({'error': 'You dont have enough coins!'})
                team.coins += int(coins)
                current_user.coins -= int(coins)
                db.session.commit()
            except ValueError:
                return jsonify({'error': 'Invalid coin value!'})

    return render_template('terminal.html')
