from flask import render_template, session, redirect, url_for
from app import webapp
from os import urandom


webapp.secret_key = urandom(24)


@webapp.route("/")
def index():
    if 'authorized' in session and session['authorized'] is True:
        return redirect(url_for("welcome"))

    return render_template("index.html")
