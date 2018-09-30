from flask import render_template, Flask, redirect, url_for
from flask import g as user_data
from app import webapp
from os import urandom


webapp.secret_key = urandom(24)


@webapp.route("/")
def index():
    if user_data.authorized is True:
        return redirect(url_for("welcome"))

    return render_template("index.html")
