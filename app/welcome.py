from flask import render_template, request, session, redirect, url_for
from flask import g as user_data
from app.tools.pwdManager import PwdManager
from app import webapp


@webapp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    # TODO: The hashing shouldn't be here. Move to "create new account"
    pwd_manager = PwdManager()
    salt, hashpwd = pwd_manager.get_salt_hash(password)#[1]

    if pwd_manager.check_password(username, password):
        session['user'] = username
        session['authorized'] = True
        return redirect(url_for('welcome'))

    return render_template("index.html", error=True, username=username)


@webapp.route('/welcome')
def welcome():
    if user_data.authorized is True:
        return render_template('welcome.html', username=user_data.user)

    return redirect(url_for('index'))