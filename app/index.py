from typing import Any, Union

from flask import render_template, url_for, request
from app import webapp
from hashlib import pbkdf2_hmac
from os import urandom
from binascii import hexlify
import smtplib

import datetime


@webapp.route("/")
def index():
    time = datetime.datetime.now()
    return render_template("index.html", time=time)


@webapp.route("/login_submit", methods=["POST"])
def login_submit():
    username = request.form.get("username")
    password = request.form.get("password")

    salt = urandom(16)
    dk = pbkdf2_hmac("sha512", password.encode(), salt, 100000)
    hashpwd = hexlify(dk)
    
    return render_template("welcome.html", username=username, password=password, salt=salt, hashpwd=hashpwd)


@webapp.route("/forgotpwd")
def forgotpwd():
    return render_template("forgotpwd.html")


@webapp.route("/recovery_submit", methods=["POST"])
def recovery_submit():
    email = request.form.get("email")

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login("ece1779.project.fall.2018", "aSd123qWe456zxc")
    msg = """
    Testing password recovery!"""

    server.sendmail("ece1779.project.fall.2018@gmail.com", email, msg)

    return render_template("index.html")