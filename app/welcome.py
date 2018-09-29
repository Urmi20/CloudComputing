from flask import render_template, request
from app.pwdManager import PwdObfuscation
from app import webapp


@webapp.route("/login_submit", methods=["POST"])
def login_submit():
    username = request.form.get("username")
    password = request.form.get("password")

    pwd_obfuscation = PwdObfuscation()
    hashpwd, salt = pwd_obfuscation.getSaltedHash(password)

    return render_template("welcome.html", username=username, password=password, salt=salt, hashpwd=hashpwd)