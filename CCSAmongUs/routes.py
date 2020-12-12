from flask import json, render_template, url_for, flash, redirect, request, jsonify
from CCSAmongUs import app, db
from CCSAmongUs.forms import RegisterationForm, LoginForm, MemberRegisterForm
from CCSAmongUs.models import Team, User, Questions, Transactions, Answerlog, Answer, Reportlog
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from pytz import timezone, utc
from sqlalchemy.exc import IntegrityError


TARGET_TIME = datetime.strptime(
    "2020-11-13 17:00:00+0530", "%Y-%m-%d %H:%M:%S%z")

TARGET_TIME_UTC = TARGET_TIME.astimezone(tz=utc)

JS_TIME_STRING_UTC = datetime.strftime(
    TARGET_TIME_UTC, "%Y-%m-%dT%H:%M:%S+00:00")


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if datetime.now(tz=utc) < TARGET_TIME_UTC:
        return redirect(url_for('preEvent'))

    if current_user.is_authenticated:
        return redirect(url_for('terminal'))
    form = LoginForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(teamname=form.teamname.data).first()
        if team and team.password == form.password.data:
            login_user(team)
            return redirect(url_for('terminal'))
    return render_template('login.html', form=form)


@app.route("/preEvent", methods=['GET', 'POST'])
def preEvent():
    if datetime.now(tz=utc) > TARGET_TIME_UTC:
        return redirect(url_for('login'))
    return render_template('preEvent.html', TIME_STRING_UTC=JS_TIME_STRING_UTC)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if datetime.now(tz=utc) < TARGET_TIME_UTC:
        return redirect(url_for('preEvent'))

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
        try:
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
        except IntegrityError:
            flash(" ")
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

        if request.form['command'] == 'team':
            user = User.query.filter_by(team=current_user.teamname).all()
            output=f"Team Name: {current_user.teamname}\nScore: {current_user.score}\nCoins: {current_user.coins}"
            if len(user) > 0:
                output += f"\nMember 1: {user[0].name}\nMember 2: {user[1].name}"
            if len(user) > 2:
                output += f"\nMember 3: {user[2].name}"
            return jsonify({'data': output})
        

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

                a_check = Answer.query.filter_by(
                    team=current_user.teamname, question=num).first()
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
                    message = "You got 100 points and 100 coins!"
                    current_user.score += 100
                    current_user.coins += 100

                db.session.add(Answer(team=current_user.teamname, question=num, answer=answer, check=check,
                                      token=datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata'))))
                db.session.commit()
                return jsonify({'status': status, 'message': message})

            except ValueError:
                return jsonify({'error': 'Invalid question value!'})

        if request.form['command'] == 'report':
            reporting_team = current_user.teamname
            reported = request.form['team']
            answer = request.form['answer']
            q = request.form['q']
            try:
                q = int(q)
                question = Questions.query.filter_by(id=q).first()

                if question == None:
                    return jsonify({'error': 'Wrong question number!'})

                r_check = Reportlog.query.filter_by(
                    reporter=reporting_team, imposter=reported, question=q).first()

                if r_check != None:
                    error = f"You have already reported {reported} for question {q}."
                    return jsonify({'error': error})

                log = Answerlog.query.filter_by(
                    giving_team=reported, receiving_team=reporting_team, question=q, answer=answer).order_by('token').first()
                submited = Answer.query.filter_by(
                    team=reporting_team, question=q).first()

                if log == None:
                    error = f"Report unsuccessful. No transaction for answer = \"{answer}\" with team = {reported} found."
                    return jsonify({'error': error})

                time_diff = -1 if submited is not None and submited.token > log.token else 1

                if time_diff < 0:
                    error = f"Report unsuccessful. Cannot report once answer is submitted after transaction."
                    return jsonify({'error': error})
                else:
                    reported_team = Team.query.filter_by(
                        teamname=reported).first()
                    transaction = Transactions.query.filter_by(
                        sender=reporting_team, receiver=reported, question_number=q).first()

                    if transaction == None:
                        error = f"No transaction took place between your team and {reported}."
                        return jsonify({"error": error})

                    coins = transaction.amount
                    db.session.add(Reportlog(reporter=reporting_team, imposter=reported, question=q, received_answer=answer, token=datetime.now(
                        timezone('UTC')).astimezone(timezone('Asia/Kolkata'))))

                    if answer != question.answer:
                        current_user.coins += (.7 * coins)
                        reported_team.coins -= (1.5 * coins)
                        current_user.score += 50
                        reported_team.report_count += 1
                        db.session.commit()
                        message = f"Report successful. You have been awarded 50 points and a refund of 70% of the transaction value i.e {.7 * coins}"
                        return jsonify({'message': message})
                    else:
                        if submited is not None:
                            submited.answer = answer
                            submited.check = 1
                        else:
                            db.session.add(Answer(team=reporting_team, question=q, answer=answer, check=1, token=datetime.now(
                                timezone('UTC')).astimezone(timezone('Asia/Kolkata'))))
                        db.session.commit()

                        message = f"Report unsuccessful. The received answer was correct. You have not been awararded any points or coins and your answer for this question has been marked correct. You may sell this answer for coins."
                        return jsonify({'message': message})

            except ValueError:
                return jsonify({'error': 'Invalid question value!'})

        if request.form['command'] == 'show_leaderboard':
            data = {}
            c = 0
            leaderboard = Team.query.order_by(Team.score.desc()).all()
            if current_user.teamname == 'admin@CCS':
                for i in leaderboard:
                    if i.teamname == 'admin@CCS':
                        continue
                    i.totalScore = (i.score * .6) + (i.coins * .4)
                db.session.commit()
                leaderboard = Team.query.order_by(Team.totalScore.desc()).all()
                for i in leaderboard:
                    if leaderboard[c].teamname == 'admin@CCS':
                        continue
                    dash = (28 - len(leaderboard[c].teamname)) * '-'
                    dash2 = (10 - len(str(leaderboard[c].totalScore))) * '-'
                    data[f"{c+1}"] = f"{leaderboard[c].teamname} {dash} {leaderboard[c].totalScore} {dash2} {leaderboard[c].report_count}"
                    c += 1
            else:
                for i in leaderboard:
                    if leaderboard[c].teamname == 'admin@CCS':
                        continue
                    dash = (28 - len(leaderboard[c].teamname)) * '-'
                    dash2 = (10 - len(str(leaderboard[c].score))) * '-'
                    data[f"{c+1}"] = f"{leaderboard[c].teamname} {dash} {leaderboard[c].score} {dash2} {leaderboard[c].report_count}"
                    c += 1
            return jsonify({'data': data})

        if request.form['command'] == 'whs':
            try:
                num = int(request.form['q_num'])
                data = {}
                c = 0
                leaderboard = Answer.query.filter_by(
                    question=num, check=1).order_by(Answer.token).all()

                if leaderboard == None:
                    raise ValueError

                for i in leaderboard:
                    if leaderboard[c].team == 'admin@CCS':
                        continue
                    data[f"{c+1}"] = f"{leaderboard[c].team}"
                    c += 1
                return jsonify({'data': data})
            except ValueError:
                return jsonify({'error': 'Invalid Question number'})

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
            q = request.form['q']

            if team == None:
                return jsonify({'error': 'Team does not exists!'})
            if team.teamname == current_user.teamname:
                return jsonify({'error': 'Cannot send coins to self!'})

            try:
                q = int(q)
                question = Questions.query.filter_by(id=q).first()

                if question == None:
                    return jsonify({'error': 'Wrong question number!'})

                transaction_check = Transactions.query.filter_by(
                    sender=current_user.teamname, receiver=team2, question_number=q).first()
                if transaction_check is not None:
                    return jsonify({'error': 'Transaction limit reached. Cannot transact with the same team for the same question more than once.'})

                if current_user.coins < int(coins):
                    return jsonify({'error': 'You dont have enough coins!'})
                team.coins += int(coins)
                current_user.coins -= int(coins)
                transaction = Transactions(sender=current_user.teamname, question_number=q, amount=int(
                    coins), receiver=team2, token=datetime.now(timezone('UTC')).astimezone(timezone('Asia/Kolkata')))
                db.session.add(transaction)
                db.session.commit()

            except ValueError:
                return jsonify({'error': 'Invalid coin or question value!'})

        # Admin Commands
        if request.form['command'] == 'iq':
            if current_user.teamname == 'admin@CCS':
                question = request.form['question']
                answer = request.form['answer']
                message = f"question: {question} \nanswer: {answer}"
                db.session.add(Questions(question=question, answer=answer))
                db.session.commit()
                return jsonify({'message': message})
            else:
                message = f"Bohot tej ho rahe ho team {current_user.teamname}. Repetition of such act will lead to Disqualification."
                return jsonify({'message': message})

        if request.form['command'] == 'at':
            if current_user.teamname == 'admin@CCS':
                team = request.form['teamname']
                data = {}
                c = 0
                transactions_all = Transactions.query.filter_by(
                    sender=team).all()
                transactions_all += Transactions.query.filter_by(
                    receiver=team).all()
                for i in transactions_all:
                    data[
                        f"{c+1}"] = f"{transactions_all[c].sender} sent {transactions_all[c].amount} to {transactions_all[c].receiver}. Date: {transactions_all[c].token.strftime('%Y-%m-%d at %H:%M:%S')}"
                    c += 1
                return jsonify({'data': data})
            else:
                error = f"Mana kiya hai na admin commands use karne ke liye team {current_user.teamname}? Repetition of such act will lead to Disqualification."
                return jsonify({'error': error})

        if request.form['command'] == 'al':
            if current_user.teamname == 'admin@CCS':
                team = request.form['teamname']
                data = {}
                c = 0
                al_all = Answerlog.query.filter_by(
                    receiving_team=team).all()
                al_all += Answerlog.query.filter_by(
                    giving_team=team).all()
                for i in al_all:
                    data[
                        f"{c+1}"] = f"{al_all[c].receiving_team} got {al_all[c].answer} from {al_all[c].giving_team}. Date: {al_all[c].token.strftime('%Y-%m-%d at %H:%M:%S')}"
                    c += 1
                return jsonify({'data': data})
            else:
                error = f"Mana kiya hai na admin commands use karne ke liye team {current_user.teamname}? Repetition of such act will lead to Disqualification."
                return jsonify({'error': error})

        if request.form['command'] == 'show_question':
            data = {}
            c = 0
            ques_all = Questions.query.all()
            for i in ques_all:
                data[
                    f"{c+1}"] = f"{ques_all[c].question}"
                c += 1
            return jsonify({'data': data})

    return render_template('terminal.html')
