from flask import render_template, url_for, flash, redirect, request, jsonify
from CCSAmongUs import app, db
from CCSAmongUs.forms import RegisterationForm, LoginForm, MemberRegisterForm
from CCSAmongUs.models import Team, User, Questions, Transactions, Answerlog, Answer
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from pytz import timezone


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
    if request.method == 'POST':
        if request.form['command'] == 'show_transactions':
            data = {}
            c = 0
            transactions_all = Transactions.query.filter_by(
                sender=current_user.teamname).all()
            transactions_all += Transactions.query.filter_by(
                receiver=current_user.teamname).all()
            for i in transactions_all:
                data[
                    f"{c+1}"] = f"{transactions_all[c].sender} sent {transactions_all[c].amount} to {transactions_all[c].receiver}. Date: {transactions_all[c].token.strftime('%Y-%m-%d at %H:%M:%S')}"
                c += 1
            return jsonify({'data': data})

        if request.form['command'] == 'get_teamname':
            return jsonify({'user': current_user.teamname})

        if request.form['command'] == 'get_coins':
            return jsonify({'coins': current_user.coins})

        if request.form['command'] == 'logout':
            logout_user()
            return jsonify({'url': '/login'})

        if request.form['command'] == 'submit':
            answer = request.form['answer']
            q_check = request.form['q_num']
            status = "Incorrect"
            check = False
            message = "You got 0 points!"
            try:
                num = int(q_check)
                q_check = Questions.query.filter_by(id=num).first()

                if q_check == None:
                    return jsonify({'error': 'Wrong question number!'})
                
                a_check = Answer.query.filter_by(team=current_user.teamname, question=num).first()
                if a_check is not None:
                    if a_check.check == 0:
                        db.session.delete(a_check)
                        db.session.commit()

                    else:
                        message = "You have already answered this question correctly!"
                        return jsonify({'message': message})

                if q_check.answer == answer:
                    check = True
                    status = "Correct"
                    message = "You got 100 points!"
                    current_user.score += 100

                db.session.add(Answer(team=current_user.teamname, question=num, answer=answer, check=check, token=datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata'))))
                db.session.commit()
                return jsonify({'status': status, 'message': message})

            except ValueError:
                return jsonify({'error': 'Invalid question value!'})

        if request.form['command'] == 'show_leaderboard':
            data = {}
            c = 0
            leaderboard = Team.query.order_by(Team.score.desc()).all()
            for i in leaderboard:
                dash = (25 - len(leaderboard[c].teamname)) * '-'
                data[f"{c+1}"] = f"{leaderboard[c].teamname} {dash} {leaderboard[c].score}"
                c += 1
            return jsonify({'data': data})

        if request.form['command'] == 'send_answer':
            from_team = current_user.teamname
            answer = request.form['answer']
            to_team = request.form['to_team']
            question = request.form['question']
            team = Team.query.filter_by(teamname=to_team).first()

            if team == None:
                return jsonify({'error': 'Team does not exists!'})
            if team.teamname == current_user.teamname:
                return jsonify({'error': 'Cannot send answers to self!'})

            try:
                num = int(question)
                # TODO: check time also for future questions
                q_check = Questions.query.filter_by(id=num).first()

                if q_check == None:
                    return jsonify({'error': 'Wrong question number!'})

                db.session.add(Answerlog(giving_team=from_team, receiving_team=to_team, question=num,
                                         answer=answer, token=datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata'))))
                db.session.commit()

            except ValueError:
                return jsonify({'error': 'Invalid question value!'})

        if request.form['command'] == 'show_answers':
            data = {}
            c = 0
            try:
                question = int(request.form['q_num'])
                answers = Answerlog.query.filter_by(
                    receiving_team=current_user.teamname, question=question).order_by(Answerlog.token.desc()).all()
                for i in answers:
                    data[
                        f"{c+1}"] = f"Received answer = \"{answers[c].answer}\" from {answers[c].giving_team} on {answers[c].token.strftime('%Y-%m-%d at %H:%M:%S')}"
                    c += 1
                return jsonify({'data': data})

            except ValueError:
                return jsonify({'error': 'Invalid question value!'})

        if request.form['command'] == 'transact':
            coins = request.form['amount']
            team2 = request.form['team2']
            team = Team.query.filter_by(teamname=team2).first()

            if team == None:
                return jsonify({'error': 'Team does not exists!'})
            if team.teamname == current_user.teamname:
                return jsonify({'error': 'Cannot send coins to self!'})

            try:
                if current_user.coins < int(coins):
                    return jsonify({'error': 'You dont have enough coins!'})
                team.coins += int(coins)
                current_user.coins -= int(coins)
                transaction = Transactions(sender=current_user.teamname, amount=int(
                    coins), receiver=team2, token=datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata')))
                db.session.add(transaction)
                db.session.commit()
            except ValueError:
                return jsonify({'error': 'Invalid coin value!'})

    return render_template('terminal.html')
