from typing import Any, Union

from flask import render_template, url_for, request
from app import webapp
import hashlib
import os
import binascii

import datetime


@webapp.route("/")
def index():
    time = datetime.datetime.now()
    return render_template("index.html", time=time)


@webapp.route("/login_submit", methods=["POST"])
def login_submit():
    username = request.form.get("username")
    password = request.form.get("password")

    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha512", password.encode(), salt, 100000)
    hashpwd = binascii.hexlify(dk)
    
    return render_template("welcome.html", username=username, password=password, salt=salt, hashpwd=hashpwd)


@webapp.route("/forgotpwd")
def forgotpwd():
    return render_template("forgotpwd.html")