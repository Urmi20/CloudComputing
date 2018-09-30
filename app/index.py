from flask import render_template, Flask, session, request, redirect, g, url_for
from app.pwdManager import PwdObfuscation
from app import webapp
import os

webapp.Flask = Flask(__name__)
webapp.secret_key = os.urandom(24)

username = None
password = None


# TODO: Can we have our auxiliary classes in an individual foder?
@webapp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        global username
        global password
        username = request.form.get("username")
        password = request.form.get("password")

        if password == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('welcome'))
        return render_template("wrong_pwd.html")
    return render_template("index.html")


@webapp.route("/welcome")
def welcome():
    if g.user is not None:
        global username
        global password
        pwd_obfuscation = PwdObfuscation()
        hashpwd, salt = pwd_obfuscation.getsaltedhash(password)

        return render_template("welcome.html", username=username, password=password, salt=salt, hashpwd=hashpwd)
    return redirect(url_for('index'))


@webapp.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
