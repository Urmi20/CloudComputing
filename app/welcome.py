from flask import render_template, request, session, redirect, url_for
from app.tools.pwdManager import PwdManager
from app import webapp


@webapp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    pwd_manager = PwdManager()
    if pwd_manager.check_password(username, password):
        session['user'] = username
        session['authorized'] = True
        return redirect(url_for('welcome'))

    return render_template("index.html", error=True, username=username)


@webapp.route('/welcome')
def welcome():
    if session['authorized'] is True:
        return render_template('welcome.html', username=session['user'])

    return redirect(url_for('index'))