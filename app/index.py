from flask import render_template
from app import webapp


# TODO: Can we have our auxiliary classes in an individual foder?
@webapp.route("/")
def index():
    return render_template("index.html")
